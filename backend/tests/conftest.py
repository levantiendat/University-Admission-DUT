import os
import pytest
from typing import Any, Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.session import get_db
from app.models.base import Base
from app.main import app
from app.models.user import User
from app.core.security import get_password_hash

# Sử dụng database SQLite cho testing
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    # Tạo database và tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Xóa database sau khi tests hoàn thành
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db) -> Generator:
    # Override dependency để sử dụng test database
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # Xóa dependency override sau khi test xong
    app.dependency_overrides = {}

@pytest.fixture
def normal_user(db) -> User:
    """Create a normal user for testing"""
    user = User(
        name="Test User",
        email="user@example.com",
        hashed_password=get_password_hash("password123"),
        role="user",
        phone_number="0912345678"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def admin_user(db) -> User:
    """Create an admin user for testing"""
    user = User(
        name="Admin User",
        email="admin@gmail.com",
        hashed_password=get_password_hash("admin123"),
        role="admin",
        phone_number="0987654321"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def instructor_user(db) -> User:
    """Create an instructor user for testing"""
    user = User(
        name="Instructor User",
        email="instructor@example.com",
        hashed_password=get_password_hash("instructor123"),
        role="instructor",
        phone_number="0912345987"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def user_token_headers(client: TestClient, normal_user: User) -> dict:
    """Get token headers for normal user"""
    response = client.post(
        "/api/auth/login",
        data={"username": normal_user.email, "password": "password123"}
    )
    access_token = response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
def admin_token_headers(client: TestClient, admin_user: User) -> dict:
    """Get token headers for admin user"""
    response = client.post(
        "/api/auth/login",
        data={"username": admin_user.email, "password": "admin123"}
    )
    access_token = response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
def instructor_token_headers(client: TestClient, instructor_user: User) -> dict:
    """Get token headers for instructor user"""
    response = client.post(
        "/api/auth/login",
        data={"username": instructor_user.email, "password": "instructor123"}
    )
    access_token = response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}