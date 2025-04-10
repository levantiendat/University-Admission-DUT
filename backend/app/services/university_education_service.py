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


def create_course(db: Session, course: CourseCreate) -> Course:
    db_course = db.query(Course).filter(Course.name == course.name).first()
    if db_course:
        raise AlreadyExistsException("Course already exists")
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def get_course(db: Session, course_id: int) -> Course:
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise NotFoundException("Course not found")
    return db_course

def get_courses(db: Session, skip: int = 0, limit: int = 100) -> list[Course]:
    return db.query(Course).offset(skip).limit(limit).all()

def update_course(db: Session, course_id: int, course: CourseUpdate) -> Course:
    db_course = get_course(db, course_id)
    for key, value in course.dict(exclude_unset=True).items():
        setattr(db_course, key, value)
    db.commit()
    db.refresh(db_course)
    return db_course

def delete_course(db: Session, course_id: int) -> Course:
    db_course = get_course(db, course_id)
    db.delete(db_course)
    db.commit()
    return db_course

def create_major_course(db: Session, major_course: MajorCourseCreate) -> MajorCourse:
    db_major_course = db.query(MajorCourse).filter(
        MajorCourse.major_id == major_course.major_id,
        MajorCourse.year == major_course.year
    ).first()
    if db_major_course:
        raise AlreadyExistsException("Major course already exists")
    db_major_course = MajorCourse(**major_course.dict())
    db.add(db_major_course)
    db.commit()
    db.refresh(db_major_course)
    return db_major_course

def get_major_course(db: Session, major_course_id: int) -> MajorCourse:
    db_major_course = db.query(MajorCourse).filter(MajorCourse.id == major_course_id).first()
    if not db_major_course:
        raise NotFoundException("Major course not found")
    return db_major_course

def get_major_courses(db: Session, skip: int = 0, limit: int = 100) -> list[MajorCourse]:
    return db.query(MajorCourse).offset(skip).limit(limit).all()

def update_major_course(db: Session, major_course_id: int, major_course: MajorCourseUpdate) -> MajorCourse:
    db_major_course = get_major_course(db, major_course_id)
    for key, value in major_course.dict(exclude_unset=True).items():
        setattr(db_major_course, key, value)
    db.commit()
    db.refresh(db_major_course)
    return db_major_course

def delete_major_course(db: Session, major_course_id: int) -> MajorCourse:
    db_major_course = get_major_course(db, major_course_id)
    db.delete(db_major_course)
    db.commit()
    return db_major_course

def create_major_course_detail(db: Session, major_course_detail: MajorCourseDetailCreate) -> MajorCourseDetail:
    db_major_course_detail = db.query(MajorCourseDetail).filter(
        MajorCourseDetail.major_course_id == major_course_detail.major_course_id,
        MajorCourseDetail.course_id == major_course_detail.course_id,
        MajorCourseDetail.semester == major_course_detail.semester
    ).first()
    if db_major_course_detail:
        raise AlreadyExistsException("Major course detail already exists")
    db_major_course_detail = MajorCourseDetail(**major_course_detail.dict())
    db.add(db_major_course_detail)
    db.commit()
    db.refresh(db_major_course_detail)
    return db_major_course_detail

def get_major_course_detail(db: Session, major_course_detail_id: int) -> MajorCourseDetail:
    db_major_course_detail = db.query(MajorCourseDetail).filter(MajorCourseDetail.id == major_course_detail_id).first()
    if not db_major_course_detail:
        raise NotFoundException("Major course detail not found")
    return db_major_course_detail

def get_major_course_details(db: Session, skip: int = 0, limit: int = 100) -> list[MajorCourseDetail]:
    return db.query(MajorCourseDetail).offset(skip).limit(limit).all()

def update_major_course_detail(db: Session, major_course_detail_id: int, major_course_detail: MajorCourseDetailUpdate) -> MajorCourseDetail:
    db_major_course_detail = get_major_course_detail(db, major_course_detail_id)
    for key, value in major_course_detail.dict(exclude_unset=True).items():
        setattr(db_major_course_detail, key, value)
    db.commit()
    db.refresh(db_major_course_detail)
    return db_major_course_detail

def delete_major_course_detail(db: Session, major_course_detail_id: int) -> MajorCourseDetail:
    db_major_course_detail = get_major_course_detail(db, major_course_detail_id)
    db.delete(db_major_course_detail)
    db.commit()
    return db_major_course_detail

def create_course_prior_course(db: Session, course_prior_course: CoursePriorCourseCreate) -> CoursePriorCourse:
    db_course_prior_course = db.query(CoursePriorCourse).filter(
        CoursePriorCourse.major_course_detail_id == course_prior_course.major_course_detail_id,
        CoursePriorCourse.prior_course_detail_id == course_prior_course.prior_course_detail_id
    ).first()
    if db_course_prior_course:
        raise AlreadyExistsException("Course prior course already exists")
    db_course_prior_course = CoursePriorCourse(**course_prior_course.dict())
    db.add(db_course_prior_course)
    db.commit()
    db.refresh(db_course_prior_course)
    return db_course_prior_course

def get_course_prior_course(db: Session, course_prior_course_id: int) -> CoursePriorCourse:
    db_course_prior_course = db.query(CoursePriorCourse).filter(CoursePriorCourse.id == course_prior_course_id).first()
    if not db_course_prior_course:
        raise NotFoundException("Course prior course not found")
    return db_course_prior_course

def get_course_prior_courses(db: Session, skip: int = 0, limit: int = 100) -> list[CoursePriorCourse]:
    return db.query(CoursePriorCourse).offset(skip).limit(limit).all()

def update_course_prior_course(db: Session, course_prior_course_id: int, course_prior_course: CoursePriorCourseUpdate) -> CoursePriorCourse:
    db_course_prior_course = get_course_prior_course(db, course_prior_course_id)
    for key, value in course_prior_course.dict(exclude_unset=True).items():
        setattr(db_course_prior_course, key, value)
    db.commit()
    db.refresh(db_course_prior_course)
    return db_course_prior_course

def delete_course_prior_course(db: Session, course_prior_course_id: int) -> CoursePriorCourse:
    db_course_prior_course = get_course_prior_course(db, course_prior_course_id)
    db.delete(db_course_prior_course)
    db.commit()
    return db_course_prior_course

def create_course_prerequisite(db: Session, course_prerequisite: CoursePrerequisiteCreate) -> CoursePrerequisite:
    db_course_prerequisite = db.query(CoursePrerequisite).filter(
        CoursePrerequisite.major_course_detail_id == course_prerequisite.major_course_detail_id,
        CoursePrerequisite.prerequisite_major_course_detail_id == course_prerequisite.prerequisite_major_course_detail_id
    ).first()
    if db_course_prerequisite:
        raise AlreadyExistsException("Course prerequisite already exists")
    db_course_prerequisite = CoursePrerequisite(**course_prerequisite.dict())
    db.add(db_course_prerequisite)
    db.commit()
    db.refresh(db_course_prerequisite)
    return db_course_prerequisite

def get_course_prerequisite(db: Session, course_prerequisite_id: int) -> CoursePrerequisite:
    db_course_prerequisite = db.query(CoursePrerequisite).filter(CoursePrerequisite.id == course_prerequisite_id).first()
    if not db_course_prerequisite:
        raise NotFoundException("Course prerequisite not found")
    return db_course_prerequisite

def get_course_prerequisites(db: Session, skip: int = 0, limit: int = 100) -> list[CoursePrerequisite]:
    return db.query(CoursePrerequisite).offset(skip).limit(limit).all()

def update_course_prerequisite(db: Session, course_prerequisite_id: int, course_prerequisite: CoursePrerequisiteUpdate) -> CoursePrerequisite:
    db_course_prerequisite = get_course_prerequisite(db, course_prerequisite_id)
    for key, value in course_prerequisite.dict(exclude_unset=True).items():
        setattr(db_course_prerequisite, key, value)
    db.commit()
    db.refresh(db_course_prerequisite)
    return db_course_prerequisite

def delete_course_prerequisite(db: Session, course_prerequisite_id: int) -> CoursePrerequisite:
    db_course_prerequisite = get_course_prerequisite(db, course_prerequisite_id)
    db.delete(db_course_prerequisite)
    db.commit()
    return db_course_prerequisite

def create_course_corequisite(db: Session, course_corequisite: CourseCorequisiteCreate) -> CourseCorequisite:
    db_course_corequisite = db.query(CourseCorequisite).filter(
        CourseCorequisite.major_course_detail_id == course_corequisite.major_course_detail_id,
        CourseCorequisite.corequisite_major_course_detail_id == course_corequisite.corequisite_major_course_detail_id
    ).first()
    if db_course_corequisite:
        raise AlreadyExistsException("Course corequisite already exists")
    db_course_corequisite = CourseCorequisite(**course_corequisite.dict())
    db.add(db_course_corequisite)
    db.commit()
    db.refresh(db_course_corequisite)
    return db_course_corequisite

def get_course_corequisite(db: Session, course_corequisite_id: int) -> CourseCorequisite:
    db_course_corequisite = db.query(CourseCorequisite).filter(CourseCorequisite.id == course_corequisite_id).first()
    if not db_course_corequisite:
        raise NotFoundException("Course corequisite not found")
    return db_course_corequisite

def get_course_corequisites(db: Session, skip: int = 0, limit: int = 100) -> list[CourseCorequisite]:
    return db.query(CourseCorequisite).offset(skip).limit(limit).all()

def update_course_corequisite(db: Session, course_corequisite_id: int, course_corequisite: CourseCorequisiteUpdate) -> CourseCorequisite:
    db_course_corequisite = get_course_corequisite(db, course_corequisite_id)
    for key, value in course_corequisite.dict(exclude_unset=True).items():
        setattr(db_course_corequisite, key, value)
    db.commit()
    db.refresh(db_course_corequisite)
    return db_course_corequisite

def delete_course_corequisite(db: Session, course_corequisite_id: int) -> CourseCorequisite:
    db_course_corequisite = get_course_corequisite(db, course_corequisite_id)
    db.delete(db_course_corequisite)
    db.commit()
    return db_course_corequisite
