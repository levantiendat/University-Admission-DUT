import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.user import User

def test_get_current_user(client: TestClient, normal_user: User, user_token_headers: dict):
    """Test get current user endpoint"""
    response = client.get("/api/users/me", headers=user_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == normal_user.email
    assert data["name"] == normal_user.name
    assert data["role"] == "user"
    assert data["id"] == normal_user.id

def test_admin_create_user(client: TestClient, db: Session, admin_token_headers: dict, user_token_headers: dict):
    """Test admin create user endpoint"""
    # Test admin tạo user mới
    user_data = {
        "name": "Admin Created User",
        "email": "admincreated@example.com",
        "password": "password123",
        "phone_number": "0912345678"
    }
    
    # Test với role user
    headers = admin_token_headers.copy()
    headers["Role"] = "user"
    response = client.post(
        "/api/users/admin/create-user",
        json=user_data,
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["role"] == "user"
    
    # Kiểm tra user đã được thêm vào database
    user = db.query(User).filter(User.email == "admincreated@example.com").first()
    assert user is not None
    assert user.name == "Admin Created User"
    assert user.role == "user"
    
    # Test với role instructor
    user_data["email"] = "admincreated_instructor@example.com"
    headers = admin_token_headers.copy()
    headers["Role"] = "instructor"
    response = client.post(
        "/api/users/admin/create-user",
        json=user_data,
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["role"] == "instructor"
    
    # Test với không phải admin
    headers = admin_token_headers.copy()
    headers["Role"] = "user"
    response = client.post(
        "/api/users/admin/create-user",
        json=user_data,
        headers=headers
    )
    assert response.status_code == 403
    assert "Not authorized" in response.json()["detail"]
    
    # Test với role không hợp lệ
    headers = admin_token_headers.copy()
    headers["Role"] = "invalid_role"
    response = client.post(
        "/api/users/admin/create-user",
        json=user_data,
        headers=headers
    )
    assert response.status_code == 400
    assert "Role must be either 'user' or 'instructor'" in response.json()["detail"]

def test_update_user(client: TestClient, normal_user: User, user_token_headers: dict):
    """Test update user endpoint"""
    # Test update thông tin người dùng
    update_data = {
        "name": "Updated User Name",
        "phone_number": "0987654321"
    }
    
    response = client.put(
        "/api/users/update",
        json=update_data,
        headers=user_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated User Name"
    assert data["phone_number"] == "0987654321"
    assert data["email"] == normal_user.email
    
    # Test update thông tin thiếu name
    invalid_data = {
        "phone_number": "0912345678"
    }
    response = client.put(
        "/api/users/update",
        json=invalid_data,
        headers=user_token_headers
    )
    assert response.status_code == 422  # Validation error

def test_admin_update_user(client: TestClient, db: Session, normal_user: User, admin_token_headers: dict, user_token_headers: dict):
    """Test admin update user endpoint"""
    # Test admin update user bằng ID
    update_data = {
        "name": "Admin Updated User",
        "phone_number": "0912345678"
    }
    
    response = client.put(
        f"/api/users/admin/update-user/{normal_user.id}",
        json=update_data,
        headers=admin_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Admin Updated User"
    assert data["phone_number"] == "0912345678"
    
    # Test với không phải admin
    response = client.put(
        f"/api/users/admin/update-user/{normal_user.id}",
        json=update_data,
        headers=user_token_headers
    )
    assert response.status_code == 403
    assert "Not authorized" in response.json()["detail"]
    
    # Test với ID không tồn tại
    response = client.put(
        "/api/users/admin/update-user/999999",
        json=update_data,
        headers=admin_token_headers
    )
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]

def test_admin_update_user_role(client: TestClient, normal_user: User, admin_token_headers: dict, user_token_headers: dict):
    """Test admin update user role endpoint"""
    # Test admin update user role
    headers = admin_token_headers.copy()
    headers["Role"] = "instructor"
    response = client.put(
        f"/api/users/admin/update-user-role/{normal_user.id}",
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "instructor"
    
    # Test với không phải admin
    headers = admin_token_headers.copy()
    headers["Role"] = "user"
    response = client.put(
        f"/api/users/admin/update-user-role/{normal_user.id}",
        headers=headers,
    )
    assert response.status_code == 403
    assert "Not authorized" in response.json()["detail"]
    
    # Test với role không hợp lệ
    headers = admin_token_headers.copy()
    headers["Role"] = "invalid_role"
    response = client.put(
        f"/api/users/admin/update-user-role/{normal_user.id}",
        headers=headers,
    )
    assert response.status_code == 400
    assert "Role must be either 'user' or 'instructor'" in response.json()["detail"]

def test_admin_get_users(client: TestClient, admin_token_headers: dict, user_token_headers: dict):
    """Test admin get users endpoint"""
    # Test admin lấy danh sách users
    response = client.get("/api/users/admin/get-users", headers=admin_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Test với không phải admin
    response = client.get("/api/users/admin/get-users", headers=user_token_headers)
    assert response.status_code == 403
    assert "Not authorized" in response.json()["detail"]

def test_admin_get_user(client: TestClient, normal_user: User, admin_token_headers: dict, user_token_headers: dict):
    """Test admin get user endpoint"""
    # Test admin lấy thông tin user
    response = client.get(f"/api/users/admin/get-user/{normal_user.id}", headers=admin_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == normal_user.id
    assert data["email"] == normal_user.email
    
    # Test với không phải admin
    response = client.get(f"/api/users/admin/get-user/{normal_user.id}", headers=user_token_headers)
    assert response.status_code == 403
    assert "Not authorized" in response.json()["detail"]
    
    # Test với ID không tồn tại
    response = client.get("/api/users/admin/get-user/999999", headers=admin_token_headers)
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]

def test_admin_delete_user(client: TestClient, db: Session, admin_token_headers: dict, user_token_headers: dict):
    """Test admin delete user endpoint"""
    # Tạo user để xóa
    user_to_delete = User(
        name="User To Delete",
        email="delete@example.com",
        hashed_password="hashedpassword",
        role="user",
        phone_number="0912345678"
    )
    db.add(user_to_delete)
    db.commit()
    db.refresh(user_to_delete)
    
    # Test admin xóa user
    response = client.delete(f"/api/users/admin/delete-user/{user_to_delete.id}", headers=admin_token_headers)
    assert response.status_code == 200
    assert response.json()["msg"] == "User deleted successfully"
    
    # Kiểm tra user đã bị xóa
    user = db.query(User).filter(User.id == user_to_delete.id).first()
    assert user is None
    
    # Test với không phải admin
    user_to_delete = User(
        name="Another User To Delete",
        email="delete2@example.com",
        hashed_password="hashedpassword",
        role="user",
        phone_number="0912345678"
    )
    db.add(user_to_delete)
    db.commit()
    db.refresh(user_to_delete)
    
    response = client.delete(f"/api/users/admin/delete-user/{user_to_delete.id}", headers=user_token_headers)
    assert response.status_code == 403
    assert "Not authorized" in response.json()["detail"]
    
    # Test với ID không tồn tại
    response = client.delete("/api/users/admin/delete-user/999999", headers=admin_token_headers)
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]