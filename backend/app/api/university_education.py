from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import verify_access_token, create_access_token
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User

from app.models.university import Faculty, Major, AdmissionMethod, AdmissionMethodMajor
from app.models.university import Subject, SubjectScoreMethodGroup, SubjectGroupDetail, ConvertPoint, PreviousAdmission
from app.models.university import Course, MajorCourse, MajorCourseDetail, CoursePriorCourse, CoursePrerequisite, CourseCorequisite
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, AlreadyExistsException
from app.core.exceptions import ForbiddenException

from app.schemas.university import CourseCreate, CourseUpdate, MajorCourseCreate, MajorCourseUpdate
from app.schemas.university import MajorCourseDetailCreate, MajorCourseDetailUpdate
from app.schemas.university import CoursePriorCourseCreate, CoursePriorCourseUpdate
from app.schemas.university import CoursePrerequisiteCreate, CoursePrerequisiteUpdate
from app.schemas.university import CourseCorequisiteCreate, CourseCorequisiteUpdate
from app.schemas.university import CoursePriorCourseOut, CoursePrerequisiteOut, CourseCorequisiteOut

from app.services.university_education_service import create_course, get_course, get_courses, update_course, delete_course
from app.services.university_education_service import create_major_course, get_major_course, get_major_courses, update_major_course, delete_major_course
from app.services.university_education_service import create_major_course_detail, get_major_course_detail, get_major_course_details, update_major_course_detail, delete_major_course_detail
from app.services.university_education_service import create_course_prior_course, get_course_prior_course, get_course_prior_courses, update_course_prior_course, delete_course_prior_course
from app.services.university_education_service import create_course_prerequisite, get_course_prerequisite, get_course_prerequisites, update_course_prerequisite, delete_course_prerequisite
from app.services.university_education_service import create_course_corequisite, get_course_corequisite, get_course_corequisites, update_course_corequisite, delete_course_corequisite

from app.core.exceptions import NotFoundException, AlreadyExistsException, ForbiddenException
from app.models.university import Faculty, Major, AdmissionMethod, AdmissionMethodMajor
from app.models.university import Subject, SubjectScoreMethodGroup, SubjectGroupDetail, ConvertPoint
from app.models.university import PreviousAdmission, Course, MajorCourse, MajorCourseDetail
from app.models.university import CoursePriorCourse, CoursePrerequisite, CourseCorequisite

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
router = APIRouter()

@router.post("/courses", response_model=CourseCreate, status_code=201)
async def create_course_endpoint(course: CourseCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để tạo mới một học phần
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
    return await create_course(db=db, course=course)

@router.get("/courses", response_model=list[CourseCreate])
async def get_courses_endpoint(db: Session = Depends(get_db)):
    """
    API để lấy danh sách tất cả học phần
    """
    return await get_courses(db=db)

@router.get("/courses/{course_id}", response_model=CourseCreate)
async def get_course_endpoint(course_id: int, db: Session = Depends(get_db)):
    """
    API để lấy thông tin một học phần theo ID
    """
    course = await get_course(db=db, course_id=course_id)
    if not course:
        raise NotFoundException(detail="Course not found")
    return course

@router.put("/courses/{course_id}", response_model=CourseCreate)
async def update_course_endpoint(course_id: int, course: CourseUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để cập nhật thông tin một học phần theo ID
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
    return await update_course(db=db, course_id=course_id, course=course)

@router.delete("/courses/{course_id}", status_code=204)
async def delete_course_endpoint(course_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để xóa một học phần theo ID
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
    return await delete_course(db=db, course_id=course_id)

@router.post("/major_courses", response_model=MajorCourseCreate, status_code=201)
async def create_major_course_endpoint(major_course: MajorCourseCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để tạo mới Khung Chương trình đào tạo - Theo năm
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
    return await create_major_course(db=db, major_course=major_course)

@router.get("/major_courses", response_model=list[MajorCourseCreate])
async def get_major_courses_endpoint(db: Session = Depends(get_db)):
    """
    API để lấy danh sách Khung Chương trình đào tạo - Theo năm
    """
    return await get_major_courses(db=db)

@router.get("/major_courses/{major_course_id}", response_model=MajorCourseCreate)
async def get_major_course_endpoint(major_course_id: int, db: Session = Depends(get_db)):
    """
    API để lấy thông tin Khung Chương trình đào tạo - Theo năm theo ID
    """
    major_course = await get_major_course(db=db, major_course_id=major_course_id)
    if not major_course:
        raise NotFoundException(detail="Major course not found")
    return major_course

@router.put("/major_courses/{major_course_id}", response_model=MajorCourseCreate)
async def update_major_course_endpoint(major_course_id: int, major_course: MajorCourseUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để cập nhật thông tin Khung Chương trình đào tạo - Theo năm theo ID
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
    return await update_major_course(db=db, major_course_id=major_course_id, major_course=major_course)

@router.delete("/major_courses/{major_course_id}", status_code=204)
async def delete_major_course_endpoint(major_course_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để xóa Khung Chương trình đào tạo - Theo năm theo ID
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
    return await delete_major_course(db=db, major_course_id=major_course_id)

@router.post("/major_course_details", response_model=MajorCourseDetailCreate, status_code=201)
async def create_major_course_detail_endpoint(major_course_detail: MajorCourseDetailCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để tạo chi tiết từng lớp học phần trong khung chương trình
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
    return await create_major_course_detail(db=db, major_course_detail=major_course_detail)

@router.get("/major_course_details", response_model=list[MajorCourseDetailCreate])
async def get_major_course_details_endpoint(db: Session = Depends(get_db)):
    """
    API để lấy danh sách chi tiết từng lớp học phần trong khung chương trình
    """
    return await get_major_course_details(db=db)

@router.get("/major_course_details/{major_course_detail_id}", response_model=MajorCourseDetailCreate)
async def get_major_course_detail_endpoint(major_course_detail_id: int, db: Session = Depends(get_db)):
    """
    API để lấy thông tin chi tiết từng lớp học phần trong khung chương trình theo ID
    """
    major_course_detail = await get_major_course_detail(db=db, major_course_detail_id=major_course_detail_id)
    if not major_course_detail:
        raise NotFoundException(detail="Major course detail not found")
    return major_course_detail

@router.put("/major_course_details/{major_course_detail_id}", response_model=MajorCourseDetailCreate)
async def update_major_course_detail_endpoint(major_course_detail_id: int, major_course_detail: MajorCourseDetailUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để cập nhật thông tin chi tiết từng lớp học phần trong khung chương trình theo ID
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
    return await update_major_course_detail(db=db, major_course_detail_id=major_course_detail_id, major_course_detail=major_course_detail)

@router.delete("/major_course_details/{major_course_detail_id}", status_code=204)
async def delete_major_course_detail_endpoint(major_course_detail_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để xóa chi tiết từng lớp học phần trong khung chương trình theo ID
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
    return await delete_major_course_detail(db=db, major_course_detail_id=major_course_detail_id)

@router.post("/course_prior_courses", response_model=CoursePriorCourseCreate, status_code=201)
async def create_course_prior_course_endpoint(course_prior_course: CoursePriorCourseCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để tạo mới mối quan hệ giữa học phần và các học phần học trước
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
    return await create_course_prior_course(db=db, course_prior_course=course_prior_course)

@router.get("/course_prior_courses", response_model=list[CoursePriorCourseOut])
async def get_course_prior_courses_endpoint(db: Session = Depends(get_db)):
    """
    API để lấy danh sách mối quan hệ giữa học phần và các học phần học trước
    """
    return await get_course_prior_courses(db=db)

@router.get("/course_prior_courses/{course_prior_course_id}", response_model=CoursePriorCourseOut)
async def get_course_prior_course_endpoint(course_prior_course_id: int, db: Session = Depends(get_db)):
    """
    API để lấy thông tin mối quan hệ giữa học phần và các học phần học trước theo ID
    """
    course_prior_course = await get_course_prior_course(db=db, course_prior_course_id=course_prior_course_id)
    if not course_prior_course:
        raise NotFoundException(detail="Course prior course not found")
    return course_prior_course

@router.put("/course_prior_courses/{course_prior_course_id}", response_model=CoursePriorCourseOut)
async def update_course_prior_course_endpoint(course_prior_course_id: int, course_prior_course: CoursePriorCourseUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để cập nhật thông tin mối quan hệ giữa học phần và các học phần học trước theo ID
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
    return await update_course_prior_course(db=db, course_prior_course_id=course_prior_course_id, course_prior_course=course_prior_course)

@router.delete("/course_prior_courses/{course_prior_course_id}", status_code=204)
async def delete_course_prior_course_endpoint(course_prior_course_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để xóa mối quan hệ giữa học phần và các học phần học trước theo ID
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
    return await delete_course_prior_course(db=db, course_prior_course_id=course_prior_course_id)

@router.post("/course_prerequisites", response_model=CoursePrerequisiteCreate, status_code=201)
async def create_course_prerequisite_endpoint(course_prerequisite: CoursePrerequisiteCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để tạo mới mối quan hệ giữa học phần và các học phần tiên quyết
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
    return await create_course_prerequisite(db=db, course_prerequisite=course_prerequisite)

@router.get("/course_prerequisites", response_model=list[CoursePrerequisiteOut])
async def get_course_prerequisites_endpoint(db: Session = Depends(get_db)):
    """
    API để lấy danh sách mối quan hệ giữa học phần và các học phần tiên quyết
    """
    return await get_course_prerequisites(db=db)

@router.get("/course_prerequisites/{course_prerequisite_id}", response_model=CoursePrerequisiteOut)
async def get_course_prerequisite_endpoint(course_prerequisite_id: int, db: Session = Depends(get_db)):
    """
    API để lấy thông tin mối quan hệ giữa học phần và các học phần tiên quyết theo ID
    """
    course_prerequisite = await get_course_prerequisite(db=db, course_prerequisite_id=course_prerequisite_id)
    if not course_prerequisite:
        raise NotFoundException(detail="Course prerequisite not found")
    return course_prerequisite

@router.put("/course_prerequisites/{course_prerequisite_id}", response_model=CoursePrerequisiteOut)
async def update_course_prerequisite_endpoint(course_prerequisite_id: int, course_prerequisite: CoursePrerequisiteUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để cập nhật thông tin mối quan hệ giữa học phần và các học phần tiên quyết theo ID
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
    return await update_course_prerequisite(db=db, course_prerequisite_id=course_prerequisite_id, course_prerequisite=course_prerequisite)

@router.delete("/course_prerequisites/{course_prerequisite_id}", status_code=204)
async def delete_course_prerequisite_endpoint(course_prerequisite_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để xóa mối quan hệ giữa học phần và các học phần tiên quyết theo ID
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
    return await delete_course_prerequisite(db=db, course_prerequisite_id=course_prerequisite_id)

@router.post("/course_corequisites", response_model=CourseCorequisiteCreate, status_code=201)
async def create_course_corequisite_endpoint(course_corequisite: CourseCorequisiteCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để tạo mới mối quan hệ giữa học phần và các học phần song hành
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
    return await create_course_corequisite(db=db, course_corequisite=course_corequisite)

@router.get("/course_corequisites", response_model=list[CourseCorequisiteOut])
async def get_course_corequisites_endpoint(db: Session = Depends(get_db)):
    """
    API để lấy danh sách mối quan hệ giữa học phần và các học phần song hành
    """
    return await get_course_corequisites(db=db)

@router.get("/course_corequisites/{course_corequisite_id}", response_model=CourseCorequisiteOut)
async def get_course_corequisite_endpoint(course_corequisite_id: int, db: Session = Depends(get_db)):
    """
    API để lấy thông tin mối quan hệ giữa học phần và các học phần song hành theo ID
    """
    course_corequisite = await get_course_corequisite(db=db, course_corequisite_id=course_corequisite_id)
    if not course_corequisite:
        raise NotFoundException(detail="Course corequisite not found")
    return course_corequisite

@router.put("/course_corequisites/{course_corequisite_id}", response_model=CourseCorequisiteOut)
async def update_course_corequisite_endpoint(course_corequisite_id: int, course_corequisite: CourseCorequisiteUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để cập nhật thông tin mối quan hệ giữa học phần và các học phần song hành theo ID
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
    return await update_course_corequisite(db=db, course_corequisite_id=course_corequisite_id, course_corequisite=course_corequisite)

@router.delete("/course_corequisites/{course_corequisite_id}", status_code=204)
async def delete_course_corequisite_endpoint(course_corequisite_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để xóa mối quan hệ giữa học phần và các học phần song hành theo ID
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
    return await delete_course_corequisite(db=db, course_corequisite_id=course_corequisite_id)