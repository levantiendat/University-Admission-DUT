import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.user import User

def test_register_endpoint(client: TestClient, db: Session):
    """Test register endpoint"""
    # Test đăng ký thành công
    user_data = {
        "name": "Register Test User",
        "email": "register@example.com",
        "password": "password123",
        "phone_number": "0912345678"
    }
    
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["role"] == "user"
    
    # Kiểm tra user đã được thêm vào database
    user = db.query(User).filter(User.email == "register@example.com").first()
    assert user is not None
    assert user.name == "Register Test User"
    assert user.role == "user"
    
    # Test đăng ký với email đã tồn tại
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]
    
    # Test đăng ký với dữ liệu thiếu
    incomplete_data = {
        "name": "Incomplete User",
        "email": "incomplete@example.com"
        # Thiếu password
    }
    response = client.post("/api/auth/register", json=incomplete_data)
    assert response.status_code == 422  # Validation error

def test_login_endpoint(client: TestClient, normal_user: User):
    """Test login endpoint"""
    # Test đăng nhập thành công
    login_data = {
        "username": normal_user.email,
        "password": "password123"
    }
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["role"] == "user"
    
    # Test đăng nhập thất bại - sai mật khẩu
    wrong_password = {
        "username": normal_user.email,
        "password": "wrongpassword"
    }
    response = client.post("/api/auth/login", data=wrong_password)
    assert response.status_code == 400
    assert "Email or password is invalid" in response.json()["detail"]
    
    # Test đăng nhập thất bại - email không tồn tại
    non_existent_email = {
        "username": "nonexistent@example.com",
        "password": "password123"
    }
    response = client.post("/api/auth/login", data=non_existent_email)
    assert response.status_code == 400
    assert "Email or password is invalid" in response.json()["detail"]

def test_reset_password_endpoint(client: TestClient, normal_user: User, user_token_headers: dict):
    """Test reset password endpoint"""
    # Test reset password thành công
    reset_data = {
        "old_password": "password123",
        "new_password": "newpassword123"
    }
    response = client.post(
        "/api/auth/reset-password",
        json=reset_data,
        headers=user_token_headers
    )
    assert response.status_code == 200
    assert response.json()["msg"] == "Password updated successfully"
    
    # Test đăng nhập với mật khẩu mới
    login_data = {
        "username": normal_user.email,
        "password": "newpassword123"
    }
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 200
    
    # Test reset password thất bại - sai mật khẩu cũ
    reset_data_wrong_old = {
        "old_password": "password123",  # Mật khẩu cũ đã được thay đổi
        "new_password": "another_new_password"
    }
    response = client.post(
        "/api/auth/reset-password",
        json=reset_data_wrong_old,
        headers=user_token_headers
    )
    assert response.status_code == 400
    assert "Old password is incorrect" in response.json()["detail"]
    
    # Test reset password thất bại - không có token
    response = client.post(
        "/api/auth/reset-password",
        json=reset_data
    )
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]

def test_me_endpoint(client: TestClient, normal_user: User, user_token_headers: dict):
    """Test me endpoint"""
    # Test với token hợp lệ
    response = client.get(
        "/api/users/me",
        headers=user_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == normal_user.email
    assert data["name"] == normal_user.name
    assert data["role"] == "user"
    
    # Test không có token
    response = client.get("/api/users/me")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]
    
    # Test với token không hợp lệ
    response = client.get(
        "/api/users/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]