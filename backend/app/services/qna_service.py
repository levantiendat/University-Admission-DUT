from app.models.user import Question, Response
from app.models.user import User
from app.schemas.qna import QuestionCreate, QuestionUpdate, ResponseCreate, ResponseUpdate
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException, AlreadyExistsException
from app.core.exceptions import ForbiddenException
from sqlalchemy.orm import joinedload

def create_question(db: Session, question: QuestionCreate, user_id: int) -> Question:
    db_question = Question(**question.dict(), user_id=user_id)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def get_question(db: Session, question_id: int) -> dict:
    """
    Lấy thông tin câu hỏi cùng với thông tin chi tiết về người đặt câu hỏi
    """
    # Sử dụng joinedload để tải thông tin user cùng với câu hỏi
    db_question = db.query(Question).options(
        joinedload(Question.user)
    ).filter(Question.id == question_id).first()
    
    if not db_question:
        raise NotFoundException("Question not found")
    
    # Chuyển đổi kết quả thành dict để có thể thêm thông tin user
    result = db_question.__dict__
    
    # Loại bỏ các thuộc tính private của SQLAlchemy
    result = {k: v for k, v in result.items() if not k.startswith('_')}
    
    # Thêm thông tin user
    if db_question.user:
        result["user"] = {
            "id": db_question.user.id,
            "name": db_question.user.name,
            "email": db_question.user.email,
            "role": db_question.user.role
        }
    
    return result

def get_questions(db: Session, skip: int = 0, limit: int = 1000) -> list[dict]:
    """
    Lấy danh sách câu hỏi cùng với thông tin chi tiết về người đặt câu hỏi
    """
    db_questions = db.query(Question).options(
        joinedload(Question.user)
    ).offset(skip).limit(limit).all()
    
    results = []
    for question in db_questions:
        # Chuyển đổi mỗi câu hỏi thành dict
        question_dict = {k: v for k, v in question.__dict__.items() if not k.startswith('_')}
        
        # Thêm thông tin user
        if question.user:
            question_dict["user"] = {
                "id": question.user.id,
                "name": question.user.name,
                "email": question.user.email,
                "role": question.user.role
            }
        
        results.append(question_dict)
        
    return results

def update_question(db: Session, question_id: int, question_update: QuestionUpdate, user_id: int) -> Question:
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        raise NotFoundException("Question not found")
    if db_question.user_id != user_id:
        raise ForbiddenException("You do not have permission to update this question")
    
    update_data = question_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_question, key, value)
    
    db.commit()
    db.refresh(db_question)
    return db_question


def delete_question(db: Session, question_id: int, user_id: int) -> Question:
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        raise NotFoundException("Question not found")
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

def get_response(db: Session, response_id: int) -> dict:
    """
    Lấy thông tin câu trả lời cùng với thông tin chi tiết về người trả lời
    """
    db_response = db.query(Response).options(
        joinedload(Response.user)
    ).filter(Response.id == response_id).first()
    
    if not db_response:
        raise NotFoundException("Response not found")
    
    # Chuyển đổi kết quả thành dict
    result = db_response.__dict__
    
    # Loại bỏ các thuộc tính private của SQLAlchemy
    result = {k: v for k, v in result.items() if not k.startswith('_')}
    
    # Thêm thông tin user
    if db_response.user:
        result["user"] = {
            "id": db_response.user.id,
            "name": db_response.user.name,
            "email": db_response.user.email,
            "role": db_response.user.role
        }
    
    return result

def get_responses(db: Session, question_id: int, skip: int = 0, limit: int = 100) -> list[dict]:
    """
    Lấy danh sách câu trả lời cho một câu hỏi cùng với thông tin chi tiết về người trả lời và câu hỏi
    """
    db_responses = db.query(Response).options(
        joinedload(Response.user),
        joinedload(Response.question)
    ).filter(Response.question_id == question_id).offset(skip).limit(limit).all()
    
    results = []
    for response in db_responses:
        response_dict = {k: v for k, v in response.__dict__.items() if not k.startswith('_')}
        
        # Thêm thông tin user
        if response.user:
            response_dict["user"] = {
                "id": response.user.id,
                "name": response.user.name,
                "email": response.user.email,
                "role": response.user.role
            }
        
        # Thêm thông tin question (đúng định dạng)
        if response.question:
            response_dict["question"] = {
                "id": response.question.id,
                "title": getattr(response.question, "title", None),
                "body_text": getattr(response.question, "body_text", None),
                "created_at": getattr(response.question, "created_at", None),
                "updated_at": getattr(response.question, "updated_at", None),
            }
        
        results.append(response_dict)
        
    return results

def update_response(db: Session, response_id: int, response_update: ResponseUpdate, user_id: int) -> Response:
    db_response = db.query(Response).filter(Response.id == response_id).first()
    if not db_response:
        raise NotFoundException("Response not found")
    if db_response.user_id != user_id:
        raise ForbiddenException("You do not have permission to update this response")
    
    update_data = response_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_response, key, value)
    
    db.commit()
    db.refresh(db_response)
    return db_response


def delete_response(db: Session, response_id: int, user_id: int) -> Response:
    db_response = db.query(Response).filter(Response.id == response_id).first()
    if not db_response:
        raise NotFoundException("Response not found")
    if db_response.user_id != user_id:
        raise ForbiddenException("You do not have permission to delete this response")
    
    db.delete(db_response)
    db.commit()
    return db_response