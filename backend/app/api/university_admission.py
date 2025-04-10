from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import verify_access_token, create_access_token
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User
from app.schemas.university import FacultyCreate, FacultyUpdate, MajorCreate, MajorUpdate, AdmissionMethodCreate, AdmissionMethodUpdate
from app.schemas.university import AdmissionMethodOut, MajorOut, FacultyOut
from app.schemas.university import AdmissionMethodMajorCreate, AdmissionMethodMajorUpdate, SubjectCreate, SubjectUpdate, AdmissionMethodMajorOut, SubjectOut
from app.schemas.university import SubjectScoreMethodGroupCreate, SubjectScoreMethodGroupUpdate, SubjectScoreMethodGroupOut
from app.schemas.university import SubjectGroupDetailCreate, SubjectGroupDetailUpdate, ConvertPointCreate, ConvertPointUpdate, SubjectGroupDetailOut, ConvertPointOut
from app.schemas.university import PreviousAdmissionCreate, PreviousAdmissionUpdate, PreviousAdmissionOut

from app.services.university_admission_service import create_faculty, get_faculty, update_faculty, delete_faculty
from app.services.university_admission_service import create_major, get_major, update_major, delete_major
from app.services.university_admission_service import create_admission_method, get_admission_method, update_admission_method, delete_admission_method
from app.services.university_admission_service import create_admission_method_major, get_admission_method_major, update_admission_method_major, delete_admission_method_major
from app.services.university_admission_service import create_subject, get_subject, update_subject, delete_subject
from app.services.university_admission_service import create_subject_score_method_group, get_subject_score_method_group, update_subject_score_method_group, delete_subject_score_method_group
from app.services.university_admission_service import create_subject_group_detail, get_subject_group_detail, update_subject_group_detail, delete_subject_group_detail
from app.services.university_admission_service import create_convert_point, get_convert_point, update_convert_point, delete_convert_point
from app.services.university_admission_service import create_previous_admission, get_previous_admission, update_previous_admission, delete_previous_admission

from app.core.exceptions import NotFoundException, AlreadyExistsException, ForbiddenException
from app.models.university import Faculty, Major, AdmissionMethod, AdmissionMethodMajor
from app.models.university import Subject, SubjectScoreMethodGroup, SubjectGroupDetail, ConvertPoint
from app.models.university import PreviousAdmission, Course, MajorCourse, MajorCourseDetail
from app.models.university import CoursePriorCourse, CoursePrerequisite, CourseCorequisite

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
router = APIRouter()

@router.get("/faculties", response_model=list[FacultyOut])
async def get_faculties(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    faculties = get_faculty(db)
    return faculties

@router.post("/faculties", response_model=FacultyOut)
async def create_faculty_endpoint(faculty: FacultyCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
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
    faculty = create_faculty(db, faculty)
    return faculty

@router.put("/faculties/{faculty_id}", response_model=FacultyOut)
async def update_faculty_endpoint(faculty_id: int, faculty: FacultyUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
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
    faculty = update_faculty(db, faculty_id, faculty)
    return faculty

@router.delete("/faculties/{faculty_id}", response_model=FacultyOut)
async def delete_faculty_endpoint(faculty_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
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
    faculty = delete_faculty(db, faculty_id)
    return faculty

@router.get("/faculties/{faculty_id}", response_model=FacultyOut)
async def get_faculty_endpoint(faculty_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    faculty = get_faculty(db, faculty_id)
    if not faculty:
        raise NotFoundException(detail="Faculty not found")
    return faculty

@router.get("/majors", response_model=list[MajorOut])
async def get_majors(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    majors = get_major(db)
    return majors

@router.post("/majors", response_model=MajorOut)
async def create_major_endpoint(major: MajorCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
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
    major = create_major(db, major)
    return major

@router.put("/majors/{major_id}", response_model=MajorOut)
async def update_major_endpoint(major_id: int, major: MajorUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
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
    major = update_major(db, major_id, major)
    return major

@router.delete("/majors/{major_id}", response_model=MajorOut)
async def delete_major_endpoint(major_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
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
    major = delete_major(db, major_id)
    return major

@router.get("/majors/{major_id}", response_model=MajorOut)
async def get_major_endpoint(major_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    major = get_major(db, major_id)
    if not major:
        raise NotFoundException(detail="Major not found")
    return major

@router.get("/admission-methods", response_model=list[AdmissionMethodOut])
async def get_admission_methods(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    admission_methods = get_admission_method(db)
    return admission_methods

@router.post("/admission-methods", response_model=AdmissionMethodOut)
async def create_admission_method_endpoint(admission_method: AdmissionMethodCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
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
    admission_method = create_admission_method(db, admission_method)
    return admission_method

@router.put("/admission-methods/{admission_method_id}", response_model=AdmissionMethodOut)
async def update_admission_method_endpoint(admission_method_id: int, admission_method: AdmissionMethodUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
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
    admission_method = update_admission_method(db, admission_method_id, admission_method)
    return admission_method

@router.delete("/admission-methods/{admission_method_id}", response_model=AdmissionMethodOut)
async def delete_admission_method_endpoint(admission_method_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
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
    admission_method = delete_admission_method(db, admission_method_id)
    return admission_method

@router.get("/admission-methods/{admission_method_id}", response_model=AdmissionMethodOut)
async def get_admission_method_endpoint(admission_method_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    admission_method = get_admission_method(db, admission_method_id)
    if not admission_method:
        raise NotFoundException(detail="Admission method not found")
    return admission_method

