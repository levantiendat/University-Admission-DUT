from app.models.user import Question, Response
from app.models.user import User
from app.schemas.qna import QuestionCreate, QuestionUpdate, ResponseCreate, ResponseUpdate
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException, AlreadyExistsException
from app.core.exceptions import ForbiddenException

def create_question(db: Session, question: QuestionCreate, user_id: int) -> Question:
    db_question = Question(**question.dict(), user_id=user_id)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def get_question(db: Session, question_id: int) -> Question:
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        raise NotFoundException("Question not found")
    return db_question

def get_questions(db: Session, skip: int = 0, limit: int = 100) -> list[Question]:
    return db.query(Question).offset(skip).limit(limit).all()

def update_question(db: Session, question_id: int, question: QuestionUpdate, user_id: int) -> Question:
    db_question = get_question(db, question_id)
    if db_question.user_id != user_id:
        raise ForbiddenException("You do not have permission to update this question")
    for key, value in question.dict(exclude_unset=True).items():
        setattr(db_question, key, value)
    db.commit()
    db.refresh(db_question)
    return db_question

def delete_question(db: Session, question_id: int, user_id: int) -> Question:
    db_question = get_question(db, question_id)
    if db_question.user_id != user_id:
        raise ForbiddenException("You do not have permission to delete this question")
    db.delete(db_question)
    db.commit()
    return db_question

def create_response(db: Session, response: ResponseCreate, user_id: int) -> Response:
    db_response = Response(**response.dict(), user_id=user_id)
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response

def get_response(db: Session, response_id: int) -> Response:
    db_response = db.query(Response).filter(Response.id == response_id).first()
    if not db_response:
        raise NotFoundException("Response not found")
    return db_response

def get_responses(db: Session, question_id: int, skip: int = 0, limit: int = 100) -> list[Response]:
    return db.query(Response).filter(Response.question_id == question_id).offset(skip).limit(limit).all()

def update_response(db: Session, response_id: int, response: ResponseUpdate, user_id: int) -> Response:
    db_response = get_response(db, response_id)
    if db_response.user_id != user_id:
        raise ForbiddenException("You do not have permission to update this response")
    for key, value in response.dict(exclude_unset=True).items():
        setattr(db_response, key, value)
    db.commit()
    db.refresh(db_response)
    return db_response

def delete_response(db: Session, response_id: int, user_id: int) -> Response:
    db_response = get_response(db, response_id)
    if db_response.user_id != user_id:
        raise ForbiddenException("You do not have permission to delete this response")
    db.delete(db_response)
    db.commit()
    return db_response