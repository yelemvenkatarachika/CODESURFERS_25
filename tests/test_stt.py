# tests/test_stt.py

import io
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app import app
from backend.database import Base, get_db

# Configure test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_edubot_stt.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override database dependency for tests
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

def test_stt_endpoint_with_audio_file(client):
    # Create a dummy audio file-like object (empty WAV header for test)
    wav_header = (
        b"RIFF$\x00\x00\x00WAVEfmt "  # Minimal WAV header (incomplete, but sufficient for dummy)
        b"\x10\x00\x00\x00\x01\x00\x01\x00" 
        b"\x40\x1f\x00\x00\x80>\x00\x00" 
        b"\x02\x00\x10\x00data\x00\x00\x00\x00"
    )
    audio_file = io.BytesIO(wav_header)
    audio_file.name = "test_audio.wav"  # Required attribute for UploadFile sim

    response = client.post(
        "/stt/transcribe",
        files={"audio_file": ("test_audio.wav", audio_file, "audio/wav")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "transcript" in data
    assert isinstance(data["transcript"], str)
    # Since service is a stub, transcript is static or placeholder string

def test_stt_endpoint_no_file(client):
    response = client.post("/stt/transcribe", files={})
    assert response.status_code == 422  # Unprocessable Entity due to missing file
