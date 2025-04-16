from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import verify_access_token, create_access_token
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User

from app.models.admitted_student import AdmittedStudent
from app.models.school_priority import City
from app.models.university import Major, AdmissionMethod, SubjectScoreMethodGroup
from app.core.exceptions import NotFoundException, AlreadyExistsException
from app.core.exceptions import ForbiddenException
from app.schemas.admitted_student import AdmittedStudentCreate,  AdmittedStudentUpdate, AdmittedStudentOut

from app.services.admitted_student_services import create_admitted_student, get_admitted_student, get_admitted_students, update_admitted_student, delete_admitted_student

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
router = APIRouter()

@router.get("/", response_model=list[AdmittedStudentOut])
async def get_admitted_students_endpoint(db: Session = Depends(get_db)):
    """
    API Để lấy danh sách sinh viên nhập học các khóa
    """
    admitted_students = get_admitted_students(db)
    return admitted_students

@router.post("/", response_model=AdmittedStudentOut)
async def create_admitted_student_endpoint(admitted_student: AdmittedStudentCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để tạo một sinh viên mới
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception

    if user.role != "admin":
        raise ForbiddenException(detail="You do not have permission to perform this action")
    admitted_student = create_admitted_student(db, admitted_student)
    return admitted_student

@router.put("/{admitted_student_id}", response_model=AdmittedStudentOut)
async def update_admitted_student_endpoint(admitted_student_id: int, admitted_student: AdmittedStudentUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để cập nhật sinh viên
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception

    if user.role != "admin":
        raise ForbiddenException(detail="You do not have permission to perform this action")
    admitted_student = update_admitted_student(db, admitted_student_id, admitted_student)
    return admitted_student

@router.delete("/{admitted_student_id}", response_model=AdmittedStudentOut)
async def delete_admitted_student_endpoint(admitted_student_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API Để xóa một sinh viên
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception

    if user.role != "admin":
        raise ForbiddenException(detail="You do not have permission to perform this action")
    admitted_student = delete_admitted_student(db, admitted_student_id)
    return admitted_student

@router.get("/{admitted_student_id}", response_model=AdmittedStudentOut)
async def get_admitted_student_endpoint(admitted_student_id: int, db: Session = Depends(get_db)):
    """
    API Get 1 sinh viên
    """
    admitted_student = get_admitted_student(db, admitted_student_id)
    if not admitted_student:
        raise NotFoundException(detail="Faculty not found")
    return admitted_student