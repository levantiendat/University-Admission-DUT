import pytest
from app.models.user import User
from app.core.security import get_password_hash
from sqlalchemy.orm import Session
from fastapi import Depends


def test_user_model():
    """Test User model properties and methods"""
    hashed_password = get_password_hash("testpassword")
    user = User(
        name="Test User",
        email="testuser@example.com",
        hashed_password=hashed_password,
        role="user",
        phone_number="0987654321"
    )
    
    # Test properties
    assert user.name == "Test User"
    assert user.email == "testuser@example.com"
    assert user.role == "user"
    assert user.hashed_password == hashed_password
    assert user.phone_number == "0987654321"
    
    # Test methods
    assert user.check_password("testpassword") == True
    assert user.check_password("wrongpassword") == False

def test_user_relationships(db: Session):
    """Test User relationships with other models"""
    from app.models.user import Question, Response
    
    # Create a test user
    user = User(
        name="Relation Test User",
        email="relationtest@example.com",
        hashed_password=get_password_hash("password123"),
        role="user",
        phone_number="0912345678"
    )
    db.add(user)
    db.commit()
    
    # Create a question by this user
    question = Question(
        title="Test Question",
        body_text="This is a test question",
        user_id=user.id
    )
    db.add(question)
    db.commit()
    
    # Create a response by this user
    response = Response(
        body_text="This is a test response",
        question_id=question.id,
        user_id=user.id
    )
    db.add(response)
    db.commit()
    
    # Test relationships
    db.refresh(user)
    assert len(user.questions) == 1
    assert user.questions[0].title == "Test Question"
    assert user.questions[0].body_text == "This is a test question"
    
    assert len(user.responses) == 1
    assert user.responses[0].body_text == "This is a test response"
    
    # Test cascade delete
    db.delete(user)
    db.commit()
    
    # Verify that questions and responses are also deleted
    assert db.query(Question).count() == 0
    assert db.query(Response).count() == 0