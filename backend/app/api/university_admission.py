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
from app.schemas.university import SubjectScoreMethodMajorCreate, SubjectScoreMethodMajorUpdate, SubjectScoreMethodMajorOut
from app.schemas.university import PreviousAdmissionCreate, PreviousAdmissionUpdate, PreviousAdmissionOut, ScoreCalculationResponse
from app.schemas.university import AdmissionDescriptionCreate, AdmissionDescriptionUpdate, AdmissionDescriptionOut, PointCountRequest, PointCountResponse, ScoreCalculationRequest, PriorityCalculationRequest, PriorityCalculationResponse



from app.services.university_admission_service import create_faculty, get_faculty, update_faculty, delete_faculty, get_faculties
from app.services.university_admission_service import create_major, get_major, update_major, delete_major, get_major_by_faculty, get_majors
from app.services.university_admission_service import create_admission_method, get_admission_method, update_admission_method, delete_admission_method, get_admission_methods
from app.services.university_admission_service import create_admission_method_major, get_admission_method_major, update_admission_method_major, delete_admission_method_major, get_admission_method_major_by_major, get_major_by_admission_method, get_admission_method_majors
from app.services.university_admission_service import create_subject, get_subject, update_subject, delete_subject, get_subjects
from app.services.university_admission_service import create_subject_score_method_group, get_subject_score_method_group, update_subject_score_method_group, delete_subject_score_method_group, get_subject_score_method_groups
from app.services.university_admission_service import create_subject_group_detail, get_subject_group_detail, update_subject_group_detail, delete_subject_group_detail, get_subject_group_detail_by_group, get_subject_group_details
from app.services.university_admission_service import create_subject_score_method_major, get_subject_score_method_majors, get_subject_score_method_major, update_subject_score_method_major, delete_subject_score_method_major
from app.services.university_admission_service import create_convert_point, get_convert_point, update_convert_point, delete_convert_point, get_convert_point_by_admission_method, get_convert_points
from app.services.university_admission_service import create_previous_admission, get_previous_admission, update_previous_admission, delete_previous_admission, get_previous_admission_by_major, get_previous_admission_by_admission_method,get_previous_admission_by_major_and_admission_method, get_previous_admission_by_year, get_previous_admissions 
from app.services.university_admission_service import create_admission_description, get_admission_description, update_admission_description, delete_admission_description, get_admission_descriptions, get_major_by_subject_score_method_group, calculate_admission_scores, calculate_priority_points, get_subject_score_method_major_by_major_and_admission_method, get_admission_description_by_major
from app.services.priority_service import get_school_by_id
from app.core.exceptions import NotFoundException, AlreadyExistsException, ForbiddenException
from app.models.university import Faculty, Major, AdmissionMethod, AdmissionMethodMajor
from app.models.university import Subject, SubjectScoreMethodGroup, SubjectGroupDetail, ConvertPoint
from app.models.university import PreviousAdmission, Course, MajorCourse, MajorCourseDetail
from app.models.university import CoursePriorCourse, CoursePrerequisite, CourseCorequisite

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
router = APIRouter()

@router.get("/faculties", response_model=list[FacultyOut])
async def get_faculties_endpoint(db: Session = Depends(get_db)):
    """
    API để lấy danh sách các khoa quản lý
    """
    faculties = get_faculties(db)
    return faculties

@router.post("/faculties", response_model=FacultyOut)
async def create_faculty_endpoint(faculty: FacultyCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để tạo mới một khoa quản lý
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
    faculty = create_faculty(db, faculty)
    return faculty

@router.put("/faculties/{faculty_id}", response_model=FacultyOut)
async def update_faculty_endpoint(faculty_id: int, faculty: FacultyUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để cập nhật thông tin một khoa quản lý
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
    faculty = update_faculty(db, faculty_id, faculty)
    return faculty

@router.delete("/faculties/{faculty_id}", response_model=FacultyOut)
async def delete_faculty_endpoint(faculty_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để xóa một khoa quản lý
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
    faculty = delete_faculty(db, faculty_id)
    return faculty

@router.get("/faculties/{faculty_id}", response_model=FacultyOut)
async def get_faculty_endpoint(faculty_id: int, db: Session = Depends(get_db)):
    """
    API để lấy thông tin một khoa quản lý
    """
    faculty = get_faculty(db, faculty_id)
    if not faculty:
        raise NotFoundException(detail="Faculty not found")
    return faculty

@router.get("/majors", response_model=list[MajorOut])
async def get_majors_endpoint(db: Session = Depends(get_db)):
    """
    API để lấy danh sách các ngành đào tạo
    """
    majors = get_majors(db)
    return majors

@router.post("/majors", response_model=MajorOut)
async def create_major_endpoint(major: MajorCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để tạo mới một ngành đào tạo
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
    major = create_major(db, major)
    return major

@router.put("/majors/{major_id}", response_model=MajorOut)
async def update_major_endpoint(major_id: int, major: MajorUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để cập nhật thông tin một ngành đào tạo
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
    major = update_major(db, major_id, major)
    return major

@router.delete("/majors/{major_id}", response_model=MajorOut)
async def delete_major_endpoint(major_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để xóa một ngành đào tạo
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
    major = delete_major(db, major_id)
    return major

@router.get("/majors/{major_id}", response_model=MajorOut)
async def get_major_endpoint(major_id: int, db: Session = Depends(get_db)):
    """
    API để lấy thông tin một ngành đào tạo
    """
    major = get_major(db, major_id)
    if not major:
        raise NotFoundException(detail="Major not found")
    return major

@router.get("/majors/faculty/{faculty_id}", response_model=list[MajorOut])
async def get_majors_by_faculty(faculty_id: int, db: Session = Depends(get_db)):
    """
    API để lấy danh sách các ngành đào tạo theo khoa quản lý
    """
    majors = get_major_by_faculty(db, faculty_id)
    return majors

@router.get("/admission-methods", response_model=list[AdmissionMethodOut])
async def get_admission_methods_endpoint(db: Session = Depends(get_db)):
    """
    API để lấy danh sách các phương thức tuyển sinh
    """
    admission_methods = get_admission_methods(db)
    return admission_methods

@router.post("/admission-methods", response_model=AdmissionMethodOut)
async def create_admission_method_endpoint(admission_method: AdmissionMethodCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để tạo mới một phương thức tuyển sinh
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
    admission_method = create_admission_method(db, admission_method)
    return admission_method

@router.put("/admission-methods/{admission_method_id}", response_model=AdmissionMethodOut)
async def update_admission_method_endpoint(admission_method_id: int, admission_method: AdmissionMethodUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """ 
    API để cập nhật thông tin một phương thức tuyển sinh
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
    admission_method = update_admission_method(db, admission_method_id, admission_method)
    return admission_method

@router.delete("/admission-methods/{admission_method_id}", response_model=AdmissionMethodOut)
async def delete_admission_method_endpoint(admission_method_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để xóa một phương thức tuyển sinh
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
    admission_method = delete_admission_method(db, admission_method_id)
    return admission_method

@router.get("/admission-methods/{admission_method_id}", response_model=AdmissionMethodOut)
async def get_admission_method_endpoint(admission_method_id: int, db: Session = Depends(get_db)):
    """
    API để lấy thông tin một phương thức tuyển sinh
    """
    admission_method = get_admission_method(db, admission_method_id)
    if not admission_method:
        raise NotFoundException(detail="Admission method not found")
    return admission_method

@router.get("/admission-method-majors", response_model=list[AdmissionMethodMajorOut])
async def get_admission_method_majors_endpoint(db: Session = Depends(get_db)):
    """
    API để lấy danh sách các phương thức tuyển sinh theo tất cả các ngành đào tạo
    """
    admission_method_majors = get_admission_method_majors(db)
    return admission_method_majors

@router.post("/admission-method-majors", response_model=AdmissionMethodMajorOut)
async def create_admission_method_major_endpoint(admission_method_major: AdmissionMethodMajorCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để tạo mới một phương thức tuyển sinh theo ngành đào tạo
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
    admission_method_major = create_admission_method_major(db, admission_method_major)
    return admission_method_major

@router.put("/admission-method-majors/{admission_method_major_id}", response_model=AdmissionMethodMajorOut)
async def update_admission_method_major_endpoint(admission_method_major_id: int, admission_method_major: AdmissionMethodMajorUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để cập nhật thông tin một phương thức tuyển sinh theo ngành đào tạo
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
    admission_method_major = update_admission_method_major(db, admission_method_major_id, admission_method_major)
    return admission_method_major

@router.delete("/admission-method-majors/{admission_method_major_id}", response_model=AdmissionMethodMajorOut)
async def delete_admission_method_major_endpoint(admission_method_major_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để xóa một phương thức tuyển sinh theo ngành đào tạo
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
    admission_method_major = delete_admission_method_major(db, admission_method_major_id)
    return admission_method_major

@router.get("/admission-method-majors/{admission_method_major_id}", response_model=AdmissionMethodMajorOut)
async def get_admission_method_major_endpoint(admission_method_major_id: int, db: Session = Depends(get_db)):
    """
    API để lấy thông tin một phương thức tuyển sinh theo ngành đào tạo
    """
    admission_method_major = get_admission_method_major(db, admission_method_major_id)
    if not admission_method_major:
        raise NotFoundException(detail="Admission method major not found")
    return admission_method_major

@router.get("/admission-method-majors/major/{major_id}", response_model=list[AdmissionMethodMajorOut])
async def get_admission_method_major_by_major_endpoint(major_id: int, db: Session = Depends(get_db)):
    """
    API để lấy danh sách các phương thức tuyển sinh theo ngành đào tạo
    """
    admission_method_majors = get_admission_method_major_by_major(db, major_id)
    return admission_method_majors

@router.get("/admission-method-majors/admission-method/{admission_method_id}", response_model=list[dict])
async def get_major_by_admission_method_endpoint(admission_method_id: int, db: Session = Depends(get_db)):
    """
    API để lấy danh sách các ngành đào tạo theo phương thức tuyển sinh
    """
    majors = get_major_by_admission_method(db, admission_method_id)
    return majors

@router.get("/subjects", response_model=list[SubjectOut])
async def get_subjects_endpoint(db: Session = Depends(get_db)):
    """
    API để lấy danh sách các môn học
    """
    subjects = get_subjects(db)
    return subjects

@router.post("/subjects", response_model=SubjectOut)
async def create_subject_endpoint(subject: SubjectCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để tạo mới một môn học
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
    subject = create_subject(db, subject)
    return subject

@router.put("/subjects/{subject_id}", response_model=SubjectOut)
async def update_subject_endpoint(subject_id: int, subject: SubjectUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để cập nhật thông tin một môn học
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
    subject = update_subject(db, subject_id, subject)
    return subject

@router.delete("/subjects/{subject_id}", response_model=SubjectOut)
async def delete_subject_endpoint(subject_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để xóa một môn học
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
    subject = delete_subject(db, subject_id)
    return subject

@router.get("/subjects/{subject_id}", response_model=SubjectOut)
async def get_subject_endpoint(subject_id: int, db: Session = Depends(get_db)):
    """
    API để lấy thông tin một môn học
    """
    subject = get_subject(db, subject_id)
    if not subject:
        raise NotFoundException(detail="Subject not found")
    return subject

@router.get("/subject-score-method-groups", response_model=list[SubjectScoreMethodGroupOut])
async def get_subject_score_method_groups_endpoint(db: Session = Depends(get_db)):
    """
    API để lấy danh sách các nhóm tổ hợp theo phương thức tính điểm nhóm môn học theo từng ngành
    """
    subject_score_method_groups = get_subject_score_method_groups(db)
    return subject_score_method_groups

@router.post("/subject-score-method-groups", response_model=SubjectScoreMethodGroupOut)
async def create_subject_score_method_group_endpoint(subject_score_method_group: SubjectScoreMethodGroupCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để tạo mới một nhóm tổ hợp theo phương thức tính điểm nhóm môn học theo từng ngành
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
    subject_score_method_group = create_subject_score_method_group(db, subject_score_method_group)
    return subject_score_method_group

@router.put("/subject-score-method-groups/{subject_score_method_group_id}", response_model=SubjectScoreMethodGroupOut)
async def update_subject_score_method_group_endpoint(subject_score_method_group_id: int, subject_score_method_group: SubjectScoreMethodGroupUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để cập nhật thông tin một nhóm tổ hợp theo phương thức tính điểm nhóm môn học theo từng ngành
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
    subject_score_method_group = update_subject_score_method_group(db, subject_score_method_group_id, subject_score_method_group)
    return subject_score_method_group

@router.delete("/subject-score-method-groups/{subject_score_method_group_id}", response_model=SubjectScoreMethodGroupOut)
async def delete_subject_score_method_group_endpoint(subject_score_method_group_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để xóa một nhóm tổ hợp theo phương thức tính điểm nhóm môn học theo từng ngành
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
    subject_score_method_group = delete_subject_score_method_group(db, subject_score_method_group_id)
    return subject_score_method_group

@router.get("/subject-score-method-groups/{subject_score_method_group_id}", response_model=SubjectScoreMethodGroupOut)
async def get_subject_score_method_group_endpoint(subject_score_method_group_id: int, db: Session = Depends(get_db)):
    """
    API để lấy thông tin một nhóm tổ hợp theo phương thức tính điểm nhóm môn học theo từng ngành
    """
    subject_score_method_group = get_subject_score_method_group(db, subject_score_method_group_id)
    if not subject_score_method_group:
        raise NotFoundException(detail="Subject score method group not found")
    return subject_score_method_group


@router.get("/subject-group-details", response_model=list[SubjectGroupDetailOut])
async def get_subject_group_details_endpoint(db: Session = Depends(get_db)):
    """
    API để lấy danh sách các môn trong tổ hợp môn học
    """
    subject_group_details = get_subject_group_details(db)
    return subject_group_details

@router.post("/subject-group-details", response_model=SubjectGroupDetailOut)
async def create_subject_group_detail_endpoint(subject_group_detail: SubjectGroupDetailCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để tạo mới một môn trong tổ hợp môn học
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
    subject_group_detail = create_subject_group_detail(db, subject_group_detail)
    return subject_group_detail

@router.put("/subject-group-details/{subject_group_detail_id}", response_model=SubjectGroupDetailOut)
async def update_subject_group_detail_endpoint(subject_group_detail_id: int, subject_group_detail: SubjectGroupDetailUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để cập nhật thông tin một môn trong tổ hợp môn học
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
    subject_group_detail = update_subject_group_detail(db, subject_group_detail_id, subject_group_detail)
    return subject_group_detail

@router.delete("/subject-group-details/{subject_group_detail_id}", response_model=SubjectGroupDetailOut)
async def delete_subject_group_detail_endpoint(subject_group_detail_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để xóa một môn trong tổ hợp môn học
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
    subject_group_detail = delete_subject_group_detail(db, subject_group_detail_id)
    return subject_group_detail

@router.get("/subject-group-details/{subject_group_detail_id}", response_model=SubjectGroupDetailOut)
async def get_subject_group_detail_endpoint(subject_group_detail_id: int, db: Session = Depends(get_db)):
    """
    API để lấy thông tin một môn trong tổ hợp môn học
    """
    subject_group_detail = get_subject_group_detail(db, subject_group_detail_id)
    if not subject_group_detail:
        raise NotFoundException(detail="Subject group detail not found")
    return subject_group_detail

@router.get("/subject-group-details/group/{group_id}", response_model=list[SubjectGroupDetailOut])
async def get_subject_group_detail_by_group_endpoint(group_id: int, db: Session = Depends(get_db)):
    """
    API để lấy danh sách các môn trong tổ hợp theo nhóm môn học
    """
    subject_group_details = get_subject_group_detail_by_group(db, group_id)
    return subject_group_details

@router.get("/subject-score-method-majors", response_model=list[SubjectScoreMethodMajorOut])
async def get_subject_score_method_majors_endpoint(db: Session = Depends(get_db)):
    """
    API lấy danh sách các subject score method majors
    """
    subject_score_method_majors = get_subject_score_method_majors(db)
    return subject_score_method_majors

@router.post("/subject-score-method-majors", response_model=SubjectScoreMethodMajorOut)
async def create_subject_score_method_major_endpoint(
    subject_score_method_major: SubjectScoreMethodMajorCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    API tạo mới subject score method major
    """
    # Kiểm tra token và quyền admin
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

    subject_score_method_major_db = create_subject_score_method_major(db, subject_score_method_major)
    return subject_score_method_major_db

@router.get("/subject-score-method-majors/{subject_score_method_major_id}", response_model=SubjectScoreMethodMajorOut)
async def get_subject_score_method_major_endpoint(subject_score_method_major_id: int, db: Session = Depends(get_db)):
    """
    API lấy thông tin một subject score method major theo id
    """
    subject_score_method_major_db = get_subject_score_method_major(db, subject_score_method_major_id)
    if not subject_score_method_major_db:
        raise NotFoundException(detail="Subject score method major not found")
    return subject_score_method_major_db

@router.put("/subject-score-method-majors/{subject_score_method_major_id}", response_model=SubjectScoreMethodMajorOut)
async def update_subject_score_method_major_endpoint(
    subject_score_method_major_id: int,
    subject_score_method_major: SubjectScoreMethodMajorUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    API cập nhật thông tin subject score method major
    """
    # Kiểm tra token và quyền admin
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

    updated_subject_score_method_major = update_subject_score_method_major(db, subject_score_method_major_id, subject_score_method_major)
    return updated_subject_score_method_major

@router.delete("/subject-score-method-majors/{subject_score_method_major_id}", response_model=SubjectScoreMethodMajorOut)
async def delete_subject_score_method_major_endpoint(
    subject_score_method_major_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    API xóa subject score method major
    """
    # Kiểm tra token và quyền admin
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

    deleted_subject_score_method_major = delete_subject_score_method_major(db, subject_score_method_major_id)
    return deleted_subject_score_method_major

@router.get("/subject-score-method-majors/group/{group_id}", response_model=list[dict])
async def get_major_by_subject_score_method_group_endpoint(group_id: int, db: Session = Depends(get_db)):
    """
    API lấy danh sách subject score method major theo group id
    """
    subject_score_method_majors = get_major_by_subject_score_method_group(db, group_id)
    return subject_score_method_majors

@router.get("/subject-score-method-majors/major/{major_id}/admission-method/{admission_method_id}", response_model=list[SubjectScoreMethodMajorOut])
async def get_subject_score_method_major_by_major_and_admission_method_endpoint(major_id: int, admission_method_id: int, db: Session = Depends(get_db)):
    """
    API lấy danh sách subject score method major theo major id và admission method id
    """
    subject_score_method_majors = get_subject_score_method_major_by_major_and_admission_method(db, major_id, admission_method_id)
    return subject_score_method_majors

@router.get("/convert-points", response_model=list[ConvertPointOut])
async def get_convert_points_endpoint(db: Session = Depends(get_db)):
    """
    API để lấy danh sách các bảng quy đổi điểm
    """
    convert_points = get_convert_points(db)
    return convert_points

@router.post("/convert-points", response_model=ConvertPointOut)
async def create_convert_point_endpoint(convert_point: ConvertPointCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để tạo mới một bảng quy đổi điểm
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
    convert_point = create_convert_point(db, convert_point)
    return convert_point

@router.put("/convert-points/{convert_point_id}", response_model=ConvertPointOut)
async def update_convert_point_endpoint(convert_point_id: int, convert_point: ConvertPointUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để cập nhật thông tin một bảng quy đổi điểm
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
    convert_point = update_convert_point(db, convert_point_id, convert_point)
    return convert_point

@router.delete("/convert-points/{convert_point_id}", response_model=ConvertPointOut)
async def delete_convert_point_endpoint(convert_point_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để xóa một bảng quy đổi điểm
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
    convert_point = delete_convert_point(db, convert_point_id)
    return convert_point

@router.get("/convert-points/{convert_point_id}", response_model=ConvertPointOut)
async def get_convert_point_endpoint(convert_point_id: int, db: Session = Depends(get_db)):
    """
    API để lấy thông tin một bảng quy đổi điểm
    """
    convert_point = get_convert_point(db, convert_point_id)
    if not convert_point:
        raise NotFoundException(detail="Convert point not found")
    return convert_point

@router.get("/convert-points/admission-method/{admission_method_id}", response_model=list[ConvertPointOut])
async def get_convert_point_by_admission_method(admission_method_id: int, db: Session = Depends(get_db)):
    """
    API để lấy danh sách các bảng quy đổi điểm theo phương thức tuyển sinh
    """
    convert_points = get_convert_point_by_admission_method(db, admission_method_id)
    return convert_points

@router.get("/previous-admissions", response_model=list[PreviousAdmissionOut])
async def get_previous_admissions_endpoint(db: Session = Depends(get_db)):
    """
    API để lấy danh sách các điểm chuẩn của các ngành đào tạo các năm trước
    """
    previous_admissions = get_previous_admissions(db)
    return previous_admissions

@router.post("/previous-admissions", response_model=PreviousAdmissionOut)
async def create_previous_admission_endpoint(previous_admission: PreviousAdmissionCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để tạo mới một điểm chuẩn của ngành đào tạo năm trước
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
    previous_admission = create_previous_admission(db, previous_admission)
    return previous_admission

@router.put("/previous-admissions/{previous_admission_id}", response_model=PreviousAdmissionOut)
async def update_previous_admission_endpoint(previous_admission_id: int, previous_admission: PreviousAdmissionUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để cập nhật thông tin một điểm chuẩn của ngành đào tạo năm trước
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
    previous_admission = update_previous_admission(db, previous_admission_id, previous_admission)
    return previous_admission

@router.delete("/previous-admissions/{previous_admission_id}", response_model=PreviousAdmissionOut)
async def delete_previous_admission_endpoint(previous_admission_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để xóa một điểm chuẩn của ngành đào tạo năm trước
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
    previous_admission = delete_previous_admission(db, previous_admission_id)
    return previous_admission

@router.get("/previous-admissions/{previous_admission_id}", response_model=PreviousAdmissionOut)
async def get_previous_admission_endpoint(previous_admission_id: int, db: Session = Depends(get_db)):
    """
    API để lấy thông tin một điểm chuẩn của ngành đào tạo năm trước
    """
    previous_admission = get_previous_admission(db, previous_admission_id)
    if not previous_admission:
        raise NotFoundException(detail="Previous admission not found")
    return previous_admission

@router.get("/previous-admissions/major/{major_id}", response_model=list[PreviousAdmissionOut])
async def get_previous_admission_by_majors(major_id: int, db: Session = Depends(get_db)):
    """
    API để lấy danh sách các điểm chuẩn của một ngành đào tạo năm trước
    """
    previous_admissions = get_previous_admission_by_major(db, major_id)
    return previous_admissions

@router.get("/previous-admissions/admission-method/{admission_method_id}", response_model=list[PreviousAdmissionOut])
async def get_previous_admission_by_admission_methods(admission_method_id: int, db: Session = Depends(get_db)):
    """
    API để lấy danh sách các điểm chuẩn của một phương thức tuyển sinh năm trước
    """
    previous_admissions = get_previous_admission_by_admission_method(db, admission_method_id)
    return previous_admissions

@router.get("/previous-admissions/major/{major_id}/admission-method/{admission_method_id}", response_model=list[PreviousAdmissionOut])
async def get_previous_admission_by_major_and_admission_methods(major_id: int, admission_method_id: int, db: Session = Depends(get_db)):
    """
    API để lấy danh sách các điểm chuẩn của một ngành đào tạo theo phương thức tuyển sinh năm trước
    """
    previous_admissions = get_previous_admission_by_major_and_admission_method(db, major_id, admission_method_id)
    return previous_admissions

@router.get("/previous-admissions/year/{year}", response_model=list[PreviousAdmissionOut])
async def get_previous_admission_by_years(year: int, db: Session = Depends(get_db)):
    """
    API để lấy danh sách các điểm chuẩn của các ngành đào tạo năm trước theo năm
    """
    previous_admissions = get_previous_admission_by_year(db, year)
    return previous_admissions

@router.get("/admission-descriptions", response_model=list[AdmissionDescriptionOut])
async def get_admission_descriptions_endpoint(db: Session = Depends(get_db)):
    """
    API để lấy danh sách các mô tả các lĩnh vực / môn học ở tuyển thẳng và tuyển sinh riêng
    """
    admission_descriptions = get_admission_descriptions(db)
    return admission_descriptions

@router.post("/admission-descriptions", response_model=AdmissionDescriptionOut)
async def create_admission_description_endpoint(admission_description: AdmissionDescriptionCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để tạo mới một mô tả lĩnh vực / môn học ở tuyển thẳng và tuyển sinh riêng
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
    admission_description = create_admission_description(db, admission_description)
    return admission_description

@router.put("/admission-descriptions/{admission_description_id}", response_model=AdmissionDescriptionOut)
async def update_admission_description_endpoint(admission_description_id: int, admission_description: AdmissionDescriptionUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để cập nhật thông tin một mô tả lĩnh vực / môn học ở tuyển thẳng và tuyển sinh riêng
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
    admission_description = update_admission_description(db, admission_description_id, admission_description)
    return admission_description

@router.delete("/admission-descriptions/{admission_description_id}", response_model=AdmissionDescriptionOut)
async def delete_admission_description_endpoint(admission_description_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    API để xóa một mô tả lĩnh vực / môn học ở tuyển thẳng và tuyển sinh riêng
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
    admission_description = delete_admission_description(db, admission_description_id)
    return admission_description

@router.get("/admission-descriptions/{admission_description_id}", response_model=AdmissionDescriptionOut)
async def get_admission_description_endpoint(admission_description_id: int, db: Session = Depends(get_db)):
    """
    API để lấy thông tin một mô tả lĩnh vực / môn học ở tuyển thẳng và tuyển sinh riêng
    """
    admission_description = get_admission_description(db, admission_description_id)
    if not admission_description:
        raise NotFoundException(detail="Admission description not found")
    return admission_description

@router.get("/admission-descriptions/major/{major_id}", response_model=list[AdmissionDescriptionOut])
async def get_admission_description_by_major_endpoint(major_id: int, db: Session = Depends(get_db)):
    """
    API để lấy danh sách các mô tả lĩnh vực / môn học ở tuyển thẳng và tuyển sinh riêng theo ngành
    """
    admission_descriptions = get_admission_description_by_major(db, major_id)
    return admission_descriptions

@router.post("/point-count", response_model=PointCountResponse)
async def calculate_point_count(
    data: PointCountRequest,
    db: Session = Depends(get_db),
):
    """
    API tính tổng điểm xét tuyển có và không ưu tiên dựa trên dữ liệu nhập vào.
    """

    # Tính điểm thành tích
    if data.group == "1":
        achievement_points = 30.0
    elif data.group == "2":
        mapping = {"I": 29, "II": 28, "III": 27, "Khuyến khích": 26}
        achievement_points = mapping.get(data.achievement, 0.0)
    elif data.group == "3":
        mapping = {"I": 25, "II": 24, "III": 23, "Khuyến khích": 22}
        achievement_points = mapping.get(data.achievement, 0.0)
    else:
        achievement_points = 0.0

    # Tính điểm học tập
    academic_score = 0.0
    if data.group in ["2", "3"]:
        try:
            academic_score = round((data.score10 + data.score11 + data.score12) / 30, 2)
        except:
            academic_score = 0.0

    total_non_priority = achievement_points + academic_score

    # Lấy thông tin khu vực
    area = ""
    if data.school_id:
        school = get_school_by_id(db=db, school_id=data.school_id)
        area = school["priority_area"]
    else:
        area = data.priority_area

    area_priority = {
        "KV1": 0.75,
        "KV2NT": 0.5,
        "KV2": 0.25
    }.get(area, 0.0)

    # Tính điểm ưu tiên theo đối tượng
    object_priority = 2.0 if data.priority_object in ["ĐT01", "ĐT02", "ĐT03", "ĐT04"] else \
                      1.0 if data.priority_object in ["ĐT05", "ĐT06", "ĐT07"] else 0.0

    total_priority_raw = area_priority + object_priority

    if total_non_priority < 22.5:
        converted_priority = round(total_priority_raw, 2)
    else:
        converted_priority = round(((30 - total_non_priority) / 7.5) * total_priority_raw, 2)

    total_score = round(total_non_priority + converted_priority, 2)

    return PointCountResponse(
        group=data.group,
        achievement_points=achievement_points,
        academic_score=academic_score,
        converted_priority=converted_priority,
        total_score=total_score
    )

# Add this endpoint to the existing university_admission.py

@router.post("/calculate-admission-scores", response_model=ScoreCalculationResponse)
async def calculate_admission_scores_endpoint(
    data: ScoreCalculationRequest,
    db: Session = Depends(get_db),
):
    """
    API để tính điểm xét tuyển (học bạ hoặc điểm thi THPT)
    
    - scores_type=semester: Tính điểm trung bình 6 học kỳ
    - scores_type=year: Tính điểm trung bình 3 năm học
    - scores_type=exam: Tính điểm từ kỳ thi THPT
    
    Mỗi môn học sẽ cung cấp ID hoặc tên và danh sách điểm tương ứng.
    Hệ thống sẽ tính toán kết hợp các môn học theo các tổ hợp có sẵn và trả về
    danh sách các tổ hợp có thể áp dụng với điểm tương ứng, sắp xếp theo thứ tự điểm giảm dần.
    """
    if data.scores_type not in ["semester", "year", "exam"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid scores_type. Must be 'semester' for 6 học kỳ, 'year' for 3 năm học, or 'exam' for điểm thi THPT"
        )
    
    try:
        combinations = calculate_admission_scores(db, data.scores_type, [s.dict() for s in data.subjects])
        return {"combinations": combinations}
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {str(e)}"
        )
    
@router.post("/calculate-priority", response_model=PriorityCalculationResponse)
async def calculate_priority_endpoint(
    data: PriorityCalculationRequest,
    db: Session = Depends(get_db),
):
    """
    API để tính điểm ưu tiên và tổng điểm xét tuyển
    
    Nhận điểm gốc (thang điểm 30), khu vực ưu tiên (hoặc ID trường) và đối tượng ưu tiên
    Trả về điểm gốc, điểm ưu tiên gốc, điểm ưu tiên quy đổi, và tổng điểm
    
    Nếu cung cấp school_id thì sẽ xác định khu vực ưu tiên dựa trên trường,
    nếu không thì sẽ dùng giá trị priority_area được cung cấp.
    
    Nếu điểm gốc > 22.5 thì điểm ưu tiên sẽ giảm dần theo công thức:
    ((30 - điểm gốc)/7.5) * điểm ưu tiên gốc
    """
    try:
        # Validate input
        if data.score < 0 or data.score > 30:
            raise HTTPException(
                status_code=400,
                detail="Score must be between 0 and 30"
            )
        
        if not data.school_id and not data.priority_area:
            raise HTTPException(
                status_code=400,
                detail="Either school_id or priority_area must be provided"
            )
        
        result = calculate_priority_points(
            db=db,
            score=data.score,
            priority_area=data.priority_area,
            priority_object=data.priority_object,
            school_id=data.school_id
        )
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {str(e)}"
        )