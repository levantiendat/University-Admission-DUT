import pytest
from sqlalchemy.orm import Session
from app.services.user_service import create_user, update_user
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import verify_password

def test_create_user(db: Session):
    """Test creating a new user"""
    # Test tạo user bình thường
    user_data = UserCreate(
        name="New User Service",
        email="userservice@example.com",
        password="password123",
        phone_number="0912345678"
    )
    
    user = create_user(db, user_data, "user")
    
    assert user.email == "userservice@example.com"
    assert user.name == "New User Service"
    assert user.role == "user"
    assert verify_password("password123", user.hashed_password)
    
    # Test tạo user với email đã tồn tại
    with pytest.raises(Exception) as excinfo:
        create_user(db, user_data, "user")
    assert "User already exists" in str(excinfo.value)
    

def test_update_user(db: Session):
    """Test updating a user"""
    # Tạo user để test
    user = User(
        name="Update User",
        email="updateuser@example.com",
        hashed_password="hashedpassword",
        role="user",
        phone_number="0912345678"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Update thông tin người dùng
    update_data = {
        "name": "Updated User Name",
        "phone_number": "0987654321"
    }
    
    updated_user = update_user(db, user, update_data)
    
    assert updated_user.name == "Updated User Name"
    assert updated_user.phone_number == "0987654321"
    # Các trường khác không đổi
    assert updated_user.email == "updateuser@example.com"
    assert updated_user.role == "user"
    
    # Update một số trường
    update_data = {
        "name": "Another Name Update"
    }
    
    updated_user = update_user(db, user, update_data)
    
    assert updated_user.name == "Another Name Update"
    assert updated_user.phone_number == "0987654321"