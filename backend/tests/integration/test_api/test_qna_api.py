import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.user import User, Question, Response

def test_create_question(client: TestClient, normal_user, user_token_headers):
    """Test creating a question endpoint"""
    question_data = {
        "title": "Test Question Title",
        "body_text": "This is a test question body"
    }
    
    # Test successful creation with token
    response = client.post(
        "/api/qna/questions",
        json=question_data,
        headers=user_token_headers
    )
    assert response.status_code == 201
    created_question = response.json()
    assert created_question["title"] == question_data["title"]
    assert created_question["body_text"] == question_data["body_text"]
    
    # Test creation without token (should fail)
    response = client.post("/api/qna/questions", json=question_data)
    assert response.status_code == 401

def test_get_question(client: TestClient, db: Session, normal_user, user_token_headers):
    """Test getting a question endpoint"""
    # Create a question to retrieve
    question = Question(
        title="Question to Retrieve",
        body_text="This is a question body that will be retrieved",
        user_id=normal_user.id
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    
    # Test successful retrieval with token
    response = client.get(
        f"/api/qna/questions/{question.id}",
        headers=user_token_headers
    )
    assert response.status_code == 200
    retrieved_question = response.json()
    assert retrieved_question["id"] == question.id
    assert retrieved_question["title"] == question.title
    assert retrieved_question["body_text"] == question.body_text
    assert "user" in retrieved_question
    assert retrieved_question["user"]["id"] == normal_user.id
    
    # Test retrieval without token (should fail)
    response = client.get(f"/api/qna/questions/{question.id}")
    assert response.status_code == 401
    
    # Test non-existent question ID
    response = client.get(
        "/api/qna/questions/99999",
        headers=user_token_headers
    )
    assert response.status_code == 404

def test_get_questions(client: TestClient, db: Session, normal_user, user_token_headers):
    """Test getting all questions endpoint"""
    # Create multiple questions
    questions = [
        Question(
            title=f"Test Question {i}",
            body_text=f"This is test question body {i}",
            user_id=normal_user.id
        ) for i in range(1, 4)
    ]
    for q in questions:
        db.add(q)
    db.commit()
    
    # Test successful retrieval with token
    response = client.get(
        "/api/qna/questions",
        headers=user_token_headers
    )
    assert response.status_code == 200
    questions_list = response.json()
    assert isinstance(questions_list, list)
    assert len(questions_list) >= 3
    
    # Test retrieval without token (should fail)
    response = client.get("/api/qna/questions")
    assert response.status_code == 401

def test_update_question(client: TestClient, db: Session, normal_user, user_token_headers):
    """Test updating a question endpoint"""
    # Create a question to update
    question = Question(
        title="Question to Update",
        body_text="This question will be updated",
        user_id=normal_user.id
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    
    update_data = {
        "title": "Updated Question Title",
        "body_text": "This is the updated question body"
    }
    
    # Test successful update with token
    response = client.put(
        f"/api/qna/questions/{question.id}",
        json=update_data,
        headers=user_token_headers
    )
    assert response.status_code == 200
    updated_question = response.json()
    assert updated_question["id"] == question.id
    assert updated_question["title"] == update_data["title"]
    assert updated_question["body_text"] == update_data["body_text"]
    
    # Test update without token (should fail)
    response = client.put(f"/api/qna/questions/{question.id}", json=update_data)
    assert response.status_code == 401
    
    # Test non-existent question ID
    response = client.put(
        "/api/qna/questions/99999",
        json=update_data,
        headers=user_token_headers
    )
    assert response.status_code == 404

def test_delete_question(client: TestClient, db: Session, normal_user, user_token_headers, admin_token_headers):
    """Test deleting a question endpoint"""
    # Create questions for deletion tests
    question1 = Question(
        title="Question to Delete by Owner",
        body_text="This question will be deleted by its owner",
        user_id=normal_user.id
    )
    question2 = Question(
        title="Question to Delete by Admin",
        body_text="This question will be deleted by admin",
        user_id=normal_user.id
    )
    db.add(question1)
    db.add(question2)
    db.commit()
    db.refresh(question1)
    db.refresh(question2)
    
    # Test successful deletion by owner
    response = client.delete(
        f"/api/qna/questions/{question1.id}",
        headers=user_token_headers
    )
    assert response.status_code == 200
    assert response.json()["detail"] == "Question deleted successfully"
    
    # Verify question is deleted
    assert db.query(Question).filter(Question.id == question1.id).first() is None
    
    # Test successful deletion by admin
    response = client.delete(
        f"/api/qna/questions/{question2.id}",
        headers=admin_token_headers
    )
    assert response.status_code == 200
    
    # Verify question is deleted
    assert db.query(Question).filter(Question.id == question2.id).first() is None
    
    # Test deletion without token (should fail)
    response = client.delete(f"/api/qna/questions/{question1.id}")
    assert response.status_code == 401
    
    # Test non-existent question ID
    response = client.delete(
        "/api/qna/questions/99999",
        headers=user_token_headers
    )
    assert response.status_code == 404


def test_get_response(client: TestClient, db: Session, normal_user, user_token_headers):
    """Test getting a response endpoint"""
    # Create a question and a response
    question = Question(
        title="Question with Response",
        body_text="This question has a response",
        user_id=normal_user.id
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    
    db_response = Response(
        body_text="This is a response to retrieve",
        question_id=question.id,
        user_id=normal_user.id
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    
    # Test successful retrieval with token
    api_response = client.get(
        f"/api/qna/responses/{db_response.id}",
        headers=user_token_headers
    )
    assert api_response.status_code == 200
    retrieved_response = api_response.json()
    assert retrieved_response["id"] == db_response.id
    assert retrieved_response["body_text"] == db_response.body_text
    assert retrieved_response["question_id"] == question.id
    assert "user" in retrieved_response
    
    # Test retrieval without token (should fail)
    api_response = client.get(f"/api/qna/responses/{db_response.id}")
    assert api_response.status_code == 401
    
    # Test non-existent response ID
    api_response = client.get(
        "/api/qna/responses/99999",
        headers=user_token_headers
    )
    assert api_response.status_code == 404


def test_update_response(client: TestClient, db: Session, normal_user, user_token_headers):
    """Test updating a response endpoint"""
    # Create a question and response to update
    question = Question(
        title="Question with Response to Update",
        body_text="This question has a response that will be updated",
        user_id=normal_user.id
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    
    db_response = Response(
        body_text="This response will be updated",
        question_id=question.id,
        user_id=normal_user.id
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    
    update_data = {
        "body_text": "This is the updated response text"
    }
    
    # Test successful update with token
    api_response = client.put(
        f"/api/qna/responses/{db_response.id}",
        json=update_data,
        headers=user_token_headers
    )
    assert api_response.status_code == 200
    updated_response = api_response.json()
    assert updated_response["id"] == db_response.id
    assert updated_response["body_text"] == update_data["body_text"]
    
    # Test update without token (should fail)
    api_response = client.put(f"/api/qna/responses/{db_response.id}", json=update_data)
    assert api_response.status_code == 401
    
    # Test non-existent response ID
    api_response = client.put(
        "/api/qna/responses/99999",
        json=update_data,
        headers=user_token_headers
    )
    assert api_response.status_code == 404

def test_delete_response(client: TestClient, db: Session, normal_user, user_token_headers, admin_token_headers):
    """Test deleting a response endpoint"""
    # Create question and responses for deletion tests
    question = Question(
        title="Question with Responses to Delete",
        body_text="This question has responses that will be deleted",
        user_id=normal_user.id
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    
    response1 = Response(
        body_text="Response to delete by owner",
        question_id=question.id,
        user_id=normal_user.id
    )
    response2 = Response(
        body_text="Response to delete by admin",
        question_id=question.id,
        user_id=normal_user.id
    )
    db.add(response1)
    db.add(response2)
    db.commit()
    db.refresh(response1)
    db.refresh(response2)
    
    # Test successful deletion by owner
    api_response = client.delete(
        f"/api/qna/responses/{response1.id}",
        headers=user_token_headers
    )
    assert api_response.status_code == 200
    assert api_response.json()["detail"] == "Response deleted successfully"
    
    # Verify response is deleted
    assert db.query(Response).filter(Response.id == response1.id).first() is None
    
    # Test successful deletion by admin
    api_response = client.delete(
        f"/api/qna/responses/{response2.id}",
        headers=admin_token_headers
    )
    assert api_response.status_code == 200
    
    # Verify response is deleted
    assert db.query(Response).filter(Response.id == response2.id).first() is None
    
    # Test deletion without token (should fail)
    api_response = client.delete(f"/api/qna/responses/{response1.id}")
    assert api_response.status_code == 401
    
    # Test non-existent response ID
    api_response = client.delete(
        "/api/qna/responses/99999",
        headers=user_token_headers
    )
    assert api_response.status_code == 404