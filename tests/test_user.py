# tests/test_user.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app import app
from backend.database import Base, get_db

# Setup test database (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_edubot_user.db"
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

def test_user_registration(client):
    user_data = {
        "email": "user@example.com",
        "full_name": "Test User",
        "password": "securepassword123"
    }
    response = client.post("/users/register", json=user_data)
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["email"] == user_data["email"]
    assert "id" in json_data

def test_user_login_and_token(client):
    login_data = {
        "username": "user@example.com",
        "password": "securepassword123"
    }
    response = client.post("/users/login", data=login_data)
    assert response.status_code == 200
    json_data = response.json()
    assert "access_token" in json_data
    assert json_data["token_type"] == "bearer"
    return json_data["access_token"]

def test_get_current_user_profile(client):
    token = test_user_login_and_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["email"] == "user@example.com"
    assert "id" in user_data
