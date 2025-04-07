from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException, status
from datetime import timedelta
from app.core.config import settings
import re
from fastapi.security import OAuth2PasswordBearer

def register_user(db: Session, user_in: UserCreate, role: str = "user") -> User:
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    hashed_password = get_password_hash(user_in.password)
    new_user = User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=hashed_password,
        role=role,
        phone_number=user_in.phone_number
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def is_valid_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def check_email_exists(db: Session, email: str) -> bool:
    return db.query(User).filter(User.email == email).first() is not None

def register_user_with_google(db: Session, email, name) -> User:
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return existing_user
    
    new_user = User(
        name=name,
        email=email,
        hashed_password="",
        role="user",
        phone_number="",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(db: Session, user_in: UserLogin) -> dict:
    # Check email format
    if not is_valid_email(user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or password is invalid"
        )

    user = db.query(User).filter(User.email == user_in.email).first()

    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or password is invalid"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    return {"access_token": token, "token_type": "bearer", "role": user.role}

def reset_password(db: Session, email: str, new_password: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    db.refresh(user)
    return user
