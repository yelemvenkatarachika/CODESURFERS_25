# tests/test_tts.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app import app
from backend.database import Base, get_db

# Setup test database (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_edubot_tts.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override DB dependency for isolation
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_tts_endpoint_valid_text(client):
    payload = {"text": "Hello, this is a test for text to speech."}
    response = client.post("/tts/synthesize", json=payload)
    assert response.status_code == 200
    # Check if content type is audio (depending on your implementation, might vary)
    assert response.headers["content-type"] in ["audio/mpeg", "audio/wav", "application/octet-stream"]
    audio_bytes = response.content
    assert isinstance(audio_bytes, bytes)
    assert len(audio_bytes) > 0  # Expect non-empty audio response

def test_tts_endpoint_empty_text(client):
    payload = {"text": ""}
    response = client.post("/tts/synthesize", json=payload)
    assert response.status_code == 200
    audio_bytes = response.content
    assert isinstance(audio_bytes, bytes)
    # Depending on implementation, might return silent audio or empty bytes
