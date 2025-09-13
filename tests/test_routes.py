# tests/test_routes.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app import app
from backend.database import Base, get_db

# Configure a separate SQLite test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_edubot_routes.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override database dependency for isolation
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    # Create test database schema
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as client:
        yield client
    # Drop test database schema after tests
    Base.metadata.drop_all(bind=engine)

def test_user_registration_and_login(client):
    # Register new user
    user_data = {
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "strongpassword123"
    }
    response = client.post("/users/register", json=user_data)
    assert response.status_code == 201
    resp_json = response.json()
    assert resp_json["email"] == user_data["email"]

    # Login with registered user
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    response = client.post("/users/login", data=login_data)
    assert response.status_code == 200
    tokens = response.json()
    assert "access_token" in tokens
    assert tokens["token_type"] == "bearer"

    # Use token to access protected route
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    user_info = response.json()
    assert user_info["email"] == user_data["email"]

def test_chatbot_message_flow(client):
    # Send a chatbot message
    response = client.post("/chatbot/message", json={"message": "Hello Bot!"})
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert isinstance(data["reply"], str)

def test_progress_update_and_fetch(client):
    user_id = 1  # Assuming user with ID 1 exists from previous test
    progress_payload = {
        "user_id": user_id,
        "progress": {
            "quiz_score": 90,
            "lessons_completed": 3,
            "milestones": ["Completed Lesson 1"]
        }
    }
    # Update progress
    response = client.post("/progress/update", json=progress_payload)
    assert response.status_code == 200

    # Fetch progress for user
    response = client.get(f"/progress/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["progress"]["quiz_score"] == 90

def test_quiz_get_and_evaluate(client):
    # Get quiz questions
    response = client.get("/quiz/questions")
    assert response.status_code == 200
    questions = response.json()
    assert isinstance(questions, list)

    if questions:
        question = questions[0]
        # Assuming question has options, pick one
        options = question.get("options", [])
        if options:
            option_id = options[0]["id"]
            # Evaluate answer
            answer_payload = {"question_id": question["id"], "selected_option_id": option_id}
            response = client.post("/quiz/evaluate", json=answer_payload)
            assert response.status_code == 200
            result = response.json()
            assert "correct" in result
            assert "explanation" in result

def test_text_simplification(client):
    # Test text simplification endpoint
    simplify_payload = {"text": "This is a complex sentence that needs to be simplified."}
    response = client.post("/simplify", json=simplify_payload)
    assert response.status_code == 200
    data = response.json()
    assert "simplified_text" in data
    assert isinstance(data["simplified_text"], str)
