import pytest
from sqlalchemy.orm import Session
from app.services.qna_service import (
    create_question, get_question, get_questions,
    update_question, delete_question,
    create_response, get_response, get_responses,
    update_response, delete_response
)
from app.models.user import User, Question, Response
from app.schemas.qna import QuestionCreate, QuestionUpdate, ResponseCreate, ResponseUpdate
from app.core.security import get_password_hash
from app.core.exceptions import NotFoundException, ForbiddenException

@pytest.fixture
def test_user(db: Session):
    """Create a test user for QNA tests"""
    user = User(
        name="QNA Test User",
        email="qnatest@example.com",
        hashed_password=get_password_hash("password123"),
        role="user",
        phone_number="0912345678"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def another_user(db: Session):
    """Create another user for permission testing"""
    user = User(
        name="Another User",
        email="another@example.com",
        hashed_password=get_password_hash("password123"),
        role="user",
        phone_number="0987654321"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def test_admin(db: Session):
    """Create an admin user for permission testing"""
    admin = User(
        name="Admin User",
        email="admin@example.com",
        hashed_password=get_password_hash("admin123"),
        role="admin",
        phone_number="0912345000"
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

@pytest.fixture
def test_question(db: Session, test_user):
    """Create a test question"""
    question_data = QuestionCreate(
        title="Test Question Title",
        body_text="This is a test question body"
    )
    return create_question(db, question_data, test_user.id)

@pytest.fixture
def test_response(db: Session, test_user, test_question):
    """Create a test response"""
    response_data = ResponseCreate(
        body_text="This is a test response body",
        question_id=test_question.id
    )
    return create_response(db, response_data, test_user.id)

def test_create_question(db: Session, test_user):
    """Test creating a question"""
    question_data = QuestionCreate(
        title="How to prepare for university admission?",
        body_text="I need advice on preparing for university admission exams..."
    )
    
    question = create_question(db, question_data, test_user.id)
    
    assert question.title == question_data.title
    assert question.body_text == question_data.body_text
    assert question.user_id == test_user.id
    
    # Check that question was actually added to the database
    db_question = db.query(Question).filter(Question.id == question.id).first()
    assert db_question is not None
    assert db_question.title == question_data.title

def test_get_question(db: Session, test_question):
    """Test retrieving a question by ID"""
    question = get_question(db, test_question.id)
    
    assert question["id"] == test_question.id
    assert question["title"] == test_question.title
    assert question["body_text"] == test_question.body_text
    assert "user" in question
    assert question["user"]["id"] == test_question.user_id
    
    # Test non-existent question
    with pytest.raises(NotFoundException):
        get_question(db, 99999)

def test_get_questions(db: Session, test_question):
    """Test retrieving all questions"""
    # Create a second question for testing
    another_question = Question(
        title="Another Test Question",
        body_text="This is another test question body",
        user_id=test_question.user_id
    )
    db.add(another_question)
    db.commit()
    
    questions = get_questions(db)
    
    assert len(questions) >= 2
    # Check if our test questions are in the returned list
    question_ids = [q["id"] for q in questions]
    assert test_question.id in question_ids
    assert another_question.id in question_ids

def test_update_question(db: Session, test_question, test_user, another_user):
    """Test updating a question"""
    update_data = QuestionUpdate(
        title="Updated Question Title",
        body_text="This is the updated question body"
    )
    
    # Test successful update
    updated_question = update_question(db, test_question.id, update_data, test_user.id)
    assert updated_question.title == update_data.title
    assert updated_question.body_text == update_data.body_text
    
    # Test updating with non-existent question ID
    with pytest.raises(NotFoundException):
        update_question(db, 99999, update_data, test_user.id)
    
    # Test updating another user's question (should fail)
    with pytest.raises(ForbiddenException):
        update_question(db, test_question.id, update_data, another_user.id)

def test_delete_question(db: Session, test_user, another_user, test_admin):
    """Test deleting a question"""
    # Create a question to delete
    question_to_delete = Question(
        title="Question to Delete",
        body_text="This question will be deleted",
        user_id=test_user.id
    )
    db.add(question_to_delete)
    db.commit()
    db.refresh(question_to_delete)
    
    # Test another user cannot delete the question
    with pytest.raises(ForbiddenException):
        delete_question(db, question_to_delete.id, another_user)
    
    # Create another question for admin deletion test
    another_question = Question(
        title="Another Question to Delete",
        body_text="This question will be deleted by admin",
        user_id=test_user.id
    )
    db.add(another_question)
    db.commit()
    db.refresh(another_question)
    
    # Test admin can delete any question
    deleted = delete_question(db, another_question.id, test_admin)
    assert deleted.id == another_question.id
    
    # Check question was actually deleted
    assert db.query(Question).filter(Question.id == another_question.id).first() is None
    
    # Test user can delete their own question
    deleted = delete_question(db, question_to_delete.id, test_user)
    assert deleted.id == question_to_delete.id
    
    # Check question was actually deleted
    assert db.query(Question).filter(Question.id == question_to_delete.id).first() is None
    
    # Test deleting non-existent question
    with pytest.raises(NotFoundException):
        delete_question(db, 99999, test_user)

def test_create_response(db: Session, test_user, test_question):
    """Test creating a response"""
    response_data = ResponseCreate(
        body_text="Here's some advice for your question...",
        question_id=test_question.id
    )
    
    response = create_response(db, response_data, test_user.id)
    
    assert response.body_text == response_data.body_text
    assert response.question_id == test_question.id
    assert response.user_id == test_user.id
    
    # Check response was added to database
    db_response = db.query(Response).filter(Response.id == response.id).first()
    assert db_response is not None
    assert db_response.body_text == response_data.body_text

def test_get_response(db: Session, test_response):
    """Test retrieving a response by ID"""
    response = get_response(db, test_response.id)
    
    assert response["id"] == test_response.id
    assert response["body_text"] == test_response.body_text
    assert response["question_id"] == test_response.question_id
    assert "user" in response
    assert response["user"]["id"] == test_response.user_id
    
    # Test non-existent response
    with pytest.raises(NotFoundException):
        get_response(db, 99999)

def test_get_responses(db: Session, test_question, test_response, test_user):
    """Test retrieving responses for a question"""
    # Create another response for testing
    another_response = Response(
        body_text="Another test response",
        question_id=test_question.id,
        user_id=test_user.id
    )
    db.add(another_response)
    db.commit()
    
    responses = get_responses(db, test_question.id)
    
    assert len(responses) >= 2
    # Check if our test responses are in the returned list
    response_ids = [r["id"] for r in responses]
    assert test_response.id in response_ids
    assert another_response.id in response_ids
    
    # Check that each response includes question info
    for response in responses:
        assert "question" in response
        assert response["question"]["id"] == test_question.id

def test_update_response(db: Session, test_response, test_user, another_user):
    """Test updating a response"""
    update_data = ResponseUpdate(
        body_text="This is the updated response"
    )
    
    # Test successful update
    updated_response = update_response(db, test_response.id, update_data, test_user.id)
    assert updated_response.body_text == update_data.body_text
    
    # Test updating with non-existent response ID
    with pytest.raises(NotFoundException):
        update_response(db, 99999, update_data, test_user.id)
    
    # Test updating another user's response (should fail)
    with pytest.raises(ForbiddenException):
        update_response(db, test_response.id, update_data, another_user.id)

def test_delete_response(db: Session, test_user, another_user, test_admin, test_question):
    """Test deleting a response"""
    # Create a response to delete
    response_to_delete = Response(
        body_text="Response to delete",
        question_id=test_question.id,
        user_id=test_user.id
    )
    db.add(response_to_delete)
    db.commit()
    db.refresh(response_to_delete)
    
    # Test another user cannot delete the response
    with pytest.raises(ForbiddenException):
        delete_response(db, response_to_delete.id, another_user)
    
    # Create another response for admin deletion test
    another_response = Response(
        body_text="Another response to delete",
        question_id=test_question.id,
        user_id=test_user.id
    )
    db.add(another_response)
    db.commit()
    db.refresh(another_response)
    
    # Test admin can delete any response
    deleted = delete_response(db, another_response.id, test_admin)
    assert deleted.id == another_response.id
    
    # Check response was actually deleted
    assert db.query(Response).filter(Response.id == another_response.id).first() is None
    
    # Test user can delete their own response
    deleted = delete_response(db, response_to_delete.id, test_user)
    assert deleted.id == response_to_delete.id
    
    # Check response was actually deleted
    assert db.query(Response).filter(Response.id == response_to_delete.id).first() is None
    
    # Test deleting non-existent response
    with pytest.raises(NotFoundException):
        delete_response(db, 99999, test_user)