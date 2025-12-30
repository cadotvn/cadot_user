"""
Tests for user endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_db

# Test database
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1qazxsw2@localhost/cadot_user_test"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    """Create test database and clean up after tests."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_user(test_db):
    """Test creating a new user."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "testpassword123"
    }
    
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 200
    
    user = response.json()
    assert user["email"] == user_data["email"]
    assert user["username"] == user_data["username"]
    assert user["full_name"] == user_data["full_name"]
    assert "id" in user


def test_create_user_duplicate_email(test_db):
    """Test creating user with duplicate email."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser1",
        "password": "testpassword123"
    }
    
    # Create first user
    client.post("/api/v1/users/", json=user_data)
    
    # Try to create second user with same email
    user_data["username"] = "testuser2"
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 400
    assert "email already exists" in response.json()["detail"]


def test_create_user_duplicate_username(test_db):
    """Test creating user with duplicate username."""
    user_data = {
        "email": "test1@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }
    
    # Create first user
    client.post("/api/v1/users/", json=user_data)
    
    # Try to create second user with same username
    user_data["email"] = "test2@example.com"
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 400
    assert "username already exists" in response.json()["detail"]
