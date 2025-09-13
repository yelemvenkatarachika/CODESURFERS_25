# tests/test_progress.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app import app
from backend.database import Base, get_db
from backend.services.progress_service import ProgressService
from models.progress import ProgressRequest, ProgressData

# Use a separate SQLite test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_edubot_progress.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override dependency for test DB session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Apply the override to the app
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def test_client():
    # Create test DB schema
    Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    yield client
    # Drop test DB schema after tests
    Base.metadata.drop_all(bind=engine)

def test_get_progress_empty(test_client):
    # Assume user_id 999 does not exist, expect empty progress data
    response = test_client.get("/progress/user/999")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 999
    assert data["progress"]["quiz_score"] is None
    assert data["progress"]["lessons_completed"] is None
    assert isinstance(data["progress"]["milestones"], list)

def test_update_and_get_progress(test_client):
    user_id = 101
    progress_payload = {
        "user_id": user_id,
        "progress": {
            "quiz_score": 87,
            "lessons_completed": 5,
            "milestones": ["First quiz", "Completed chapter 1"]
        }
    }
    # Update progress
    response_update = test_client.post("/progress/update", json=progress_payload)
    assert response_update.status_code == 200
    resp_data = response_update.json()
    assert resp_data["user_id"] == user_id
    assert resp_data["progress"]["quiz_score"] == 87

    # Get updated progress
    response_get = test_client.get(f"/progress/user/{user_id}")
    assert response_get.status_code == 200
    get_data = response_get.json()
    assert get_data["user_id"] == user_id
    assert get_data["progress"]["lessons_completed"] == 5
    assert "Completed chapter 1" in get_data["progress"]["milestones"]

def test_progress_service_direct(db_session=next(iter(override_get_db()))):
    service = ProgressService(db_session)
    user_id = 202
    # Test updating progress via service
    req = ProgressRequest(
        user_id=user_id,
        progress=ProgressData(
            quiz_score=95,
            lessons_completed=10,
            milestones=["Mastered topic A"]
        )
    )
    resp = service.update_progress(req)
    assert resp.user_id == user_id
    assert resp.progress.quiz_score == 95

    # Test retrieving progress via service
    resp_get = service.get_progress(user_id)
    assert resp_get.progress.lessons_completed == 10
    assert "Mastered topic A" in resp_get.progress.milestones
