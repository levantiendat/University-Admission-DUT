import pytest
from datetime import timedelta
from jose import jwt, JWTError
from app.core.security import (
    verify_password, get_password_hash, create_access_token, verify_access_token
)
from app.core.config import settings
from fastapi import HTTPException

def test_password_hash():
    """Test password hashing and verification"""
    password = "testpassword"
    hashed = get_password_hash(password)
    
    # Test hash không giống password gốc
    assert hashed != password
    
    # Test verify đúng password
    assert verify_password(password, hashed) == True
    
    # Test verify sai password
    assert verify_password("wrongpassword", hashed) == False

def test_create_access_token():
    """Test creating JWT tokens"""
    # Test token với thời gian hết hạn
    data = {"sub": "test@example.com"}
    token = create_access_token(data, expires_delta=timedelta(minutes=30))
    
    # Decode và kiểm tra nội dung
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == "test@example.com"
    assert "exp" in payload
    
    # Test token không có thời gian hết hạn (sẽ dùng giá trị mặc định)
    token = create_access_token(data)
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == "test@example.com"
    assert "exp" in payload

def test_verify_access_token():
    from datetime import timedelta
    from fastapi import HTTPException
    from app.core.security import create_access_token, verify_access_token

    # Tạo credentials_exception
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Test với token hợp lệ
    valid_data = {"sub": "test@example.com"}
    valid_token = create_access_token(data=valid_data)
    email = verify_access_token(valid_token, credentials_exception)
    assert email == "test@example.com"

    # Test với token không hợp lệ - đây là phần bị lỗi
    # Có thể token không hợp lệ không gây ra exception
    # Kiểm tra logic trong app/core/security.py

    # Đảm bảo token hoàn toàn không hợp lệ
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.wrong_signature"
    with pytest.raises(HTTPException) as excinfo:
        verify_access_token(invalid_token, credentials_exception)
    
    # Nếu hàm verify_access_token không raise exception với token không hợp lệ, 
    # cần sửa lại implementation trong app/core/security.py