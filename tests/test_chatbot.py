# tests/test_chatbot.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app import app
from backend.database import Base, get_db
from backend.services.chatbot_service import ChatbotService

# Use a separate test database for isolation
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_edubot.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use test database session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Apply the override
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def test_client():
    # Create test DB schema
    Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    yield client
    # Drop test DB schema after tests
    Base.metadata.drop_all(bind=engine)

def test_chatbot_service_generate_reply():
    # Setup ChatbotService with test session
    db = next(override_get_db())
    chatbot_service = ChatbotService(db)
    message = "Hello, EduBot!"
    reply = chatbot_service.generate_reply(message)
    assert isinstance(reply, str)
    assert message in reply  # Because mock echoes message

def test_chatbot_handle_user_message(test_client):
    response = test_client.post(
        "/chatbot/message",
        json={"message": "Hello, how are you?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert isinstance(data["reply"], str)
    assert "Hello, how are you?" in data["reply"]

def test_chatbot_session_persistence(test_client):
    # Send multiple messages and check session continuity if implemented
    msg1 = {"message": "Hi EduBot!"}
    resp1 = test_client.post("/chatbot/message", json=msg1)
    assert resp1.status_code == 200
    reply1 = resp1.json().get("reply")

    msg2 = {"message": "Tell me a joke."}
    resp2 = test_client.post("/chatbot/message", json=msg2)
    assert resp2.status_code == 200
    reply2 = resp2.json().get("reply")

    assert reply1 != reply2  # Replies should differ for different inputs
