import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.auth_service import register_user, login_user, is_valid_email, check_email_exists
from app.schemas.user import UserCreate, UserLogin
from app.models.user import User
from app.core.security import get_password_hash, verify_password

def test_register_user(db: Session):
    # Test đăng ký user mới
    user_data = UserCreate(
        name="New Test User",
        email="newuser@example.com",
        password="password123",
        phone_number="0969696969"
    )
    
    user = register_user(db, user_data)
    
    assert user.email == "newuser@example.com"
    assert user.name == "New Test User"
    assert user.role == "user"  # Default role
    assert verify_password("password123", user.hashed_password)
    
    # Test đăng ký với email đã tồn tại
    with pytest.raises(HTTPException) as excinfo:
        register_user(db, user_data)
    assert excinfo.value.status_code == 400
    assert "Email already registered" in str(excinfo.value.detail)
    
    # Test đăng ký với role khác default
    admin_data = UserCreate(
        name="Admin Test",
        email="admin_test@example.com",
        password="admin_password",
        phone_number="0912345123"
    )
    admin_user = register_user(db, admin_data, role="admin")
    assert admin_user.role == "admin"

def test_login_user(db: Session):
    # Tạo user để test
    user_data = UserCreate(
        name="Login Test User",
        email="logintest@example.com",
        password="password123",
        phone_number="0912345123"
    )
    register_user(db, user_data)
    
    # Test đăng nhập thành công
    login_data = UserLogin(
        email="logintest@example.com",
        password="password123"
    )
    result = login_user(db, login_data)
    
    assert "access_token" in result
    assert result["token_type"] == "bearer"
    assert result["role"] == "user"
    
    # Test đăng nhập thất bại - sai mật khẩu
    login_data_wrong_pass = UserLogin(
        email="logintest@example.com",
        password="wrong_password"
    )
    with pytest.raises(HTTPException) as excinfo:
        login_user(db, login_data_wrong_pass)
    assert excinfo.value.status_code == 400
    assert "Email or password is invalid" in str(excinfo.value.detail)
    
    # Test đăng nhập thất bại - email không tồn tại
    login_data_wrong_email = UserLogin(
        email="nonexistent@example.com",
        password="password123"
    )
    with pytest.raises(HTTPException) as excinfo:
        login_user(db, login_data_wrong_email)
    assert excinfo.value.status_code == 400
    assert "Email or password is invalid" in str(excinfo.value.detail)
    
    # Test đăng nhập thất bại - định dạng email không hợp lệ
    login_data_invalid_email = UserLogin(
        email="invalidemailformat",
        password="password123"
    )
    with pytest.raises(HTTPException) as excinfo:
        login_user(db, login_data_invalid_email)
    assert excinfo.value.status_code == 400
    assert "Email or password is invalid" in str(excinfo.value.detail)

def test_is_valid_email():
    # Test email hợp lệ
    assert is_valid_email("valid@example.com") == True
    assert is_valid_email("valid.email+tag@example.co.uk") == True
    
    # Test email không hợp lệ
    assert is_valid_email("invalid_email") == False
    assert is_valid_email("invalid@") == False
    assert is_valid_email("@example.com") == False
    assert is_valid_email("") == False

def test_check_email_exists(db: Session):
    # Tạo user để test
    user = User(
        name="Email Test User",
        email="emailtest@example.com",
        hashed_password=get_password_hash("password123"),
        role="user",
        phone_number="0912345678"
    )
    db.add(user)
    db.commit()
    
    # Test email tồn tại
    assert check_email_exists(db, "emailtest@example.com") == True
    
    # Test email không tồn tại
    assert check_email_exists(db, "nonexistent@example.com") == False