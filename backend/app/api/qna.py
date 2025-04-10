from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, AlreadyExistsException, ForbiddenException
from app.models.user import User
from app.db.session import get_db
from app.core.security import verify_access_token, create_access_token
from fastapi.security import OAuth2PasswordBearer
from app.schemas.qna import QuestionCreate, QuestionUpdate, ResponseCreate, ResponseUpdate, QuestionOut, ResponseOut, ResponseOutWithQuestion
from app.services.qna_service import create_question, get_question, get_questions, update_question, delete_question
from app.services.qna_service import create_response, get_response, get_responses, update_response, delete_response
from app.models.user import Question, Response

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
router = APIRouter()

@router.post("/questions", response_model=QuestionOut, status_code=201)
def create_question_endpoint(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception
    return create_question(db, question, user.id)

@router.get("/questions/{question_id}", response_model=QuestionOut)
def get_question_endpoint(
    question_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception
    return get_question(db, question_id)

@router.get("/questions", response_model=list[QuestionOut])
def get_questions_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception
    return get_questions(db, skip, limit)

@router.put("/questions/{question_id}", response_model=QuestionOut)
def update_question_endpoint(
    question_id: int,
    question: QuestionUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception
    return update_question(db, question_id, question, user.id)

@router.delete("/questions/{question_id}", response_model=QuestionOut)
def delete_question_endpoint(
    question_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception
    return delete_question(db, question_id, user.id)

@router.post("/responses", response_model=ResponseOut, status_code=201)
def create_response_endpoint(
    response: ResponseCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception
    return create_response(db, response, user.id)

@router.get("/responses/{response_id}", response_model=ResponseOut)
def get_response_endpoint(
    response_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception
    return get_response(db, response_id)

@router.get("/questions/{question_id}/responses", response_model=list[ResponseOutWithQuestion])
def get_responses_endpoint(
    question_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception
    return get_responses(db, question_id, skip, limit)

@router.put("/responses/{response_id}", response_model=ResponseOut)
def update_response_endpoint(
    response_id: int,
    response: ResponseUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception
    return update_response(db, response_id, response, user.id)

@router.delete("/responses/{response_id}", response_model=ResponseOut)
def delete_response_endpoint(
    response_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception
    return delete_response(db, response_id, user.id)