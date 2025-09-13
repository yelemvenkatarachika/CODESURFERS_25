# tests/test_simplify.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app import app
from backend.database import Base, get_db

# Setup test database (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_edubot_simplify.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override DB dependency for test isolation
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

def test_simplify_text_valid(client):
    payload = {"text": "This is a complex sentence that needs simplification."}
    response = client.post("/simplify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "simplified_text" in data
    assert isinstance(data["simplified_text"], str)

def test_simplify_text_missing_field(client):
    # Sending empty JSON should cause validation error
    response = client.post("/simplify", json={})
    assert response.status_code == 422  # Unprocessable Entity

def test_simplify_text_empty_string(client):
    payload = {"text": ""}
    response = client.post("/simplify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["simplified_text"] == "" or isinstance(data["simplified_text"], str)
