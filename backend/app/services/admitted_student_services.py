from app.models.admitted_student import AdmittedStudent
from app.models.school_priority import City
from app.models.university import Major, AdmissionMethod, SubjectScoreMethodGroup
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, AlreadyExistsException
from app.core.exceptions import ForbiddenException

from app.schemas.admitted_student import AdmittedStudentCreate,  AdmittedStudentUpdate

def create_admitted_student(db: Session, admitted_student: AdmittedStudentCreate) -> AdmittedStudent:
    db_admitted_student = db.query(AdmittedStudent).filter(AdmittedStudent.student_id == admitted_student.student_id).first()
    if db_admitted_student:
        raise AlreadyExistsException("Student already exists")
    db_admitted_student = AdmittedStudent(**admitted_student.dict())
    db.add(db_admitted_student)
    db.commit()
    db.refresh(db_admitted_student)
    return db_admitted_student

def get_admitted_student(db: Session, admitted_student_id: int) -> AdmittedStudent:
    db_admitted_student = db.query(AdmittedStudent).filter(AdmittedStudent.id == admitted_student_id).first()
    if db_admitted_student:
        raise NotFoundException("Student not found")
    return db_admitted_student

def get_admitted_students(db: Session, skip: int = 0, limit: int = 200) -> list[AdmittedStudent]:
    return db.query(AdmittedStudent).offset(skip).limit(limit).all()

def update_admitted_student(db: Session, admitted_student_id: int, admitted_student: AdmittedStudentUpdate) -> AdmittedStudent:
    db_admmited_student = get_admitted_student(db, admitted_student_id)
    for key, value in admitted_student.dict(exclude_unset=True).items():
        setattr(db_admmited_student, key, value)
    db.commit()
    db.refresh(db_admmited_student)
    return db_admmited_student

def delete_admitted_student(db: Session, admitted_student_id: int) -> AdmittedStudent:
    db_admmited_student = get_admitted_student(db, admitted_student_id)
    db.delete(db_admmited_student)
    db.commit()
    return db_admmited_student