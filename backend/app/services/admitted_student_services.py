from app.models.admitted_student import AdmittedStudent
from app.models.school_priority import City
from app.models.university import Major, AdmissionMethod, SubjectScoreMethodGroup
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, AlreadyExistsException
from app.core.exceptions import ForbiddenException
from sqlalchemy import func

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

def stats_by_gender(db: Session) -> list[dict]:
    """
    Thống kê số lượng sinh viên Nam/Nữ theo từng năm và từng ngành.
    (Giá trị AdmittedStudent.gender: 1 cho Nam, 0 cho Nữ)
    """
    results = (
        db.query(
            AdmittedStudent.year,
            AdmittedStudent.major_id,
            AdmittedStudent.gender,
            func.count(AdmittedStudent.id).label("total")
        )
        .group_by(AdmittedStudent.year, AdmittedStudent.major_id, AdmittedStudent.gender)
        .order_by(AdmittedStudent.major_id)
        .all()
    )
    return [
        {
            "year": r.year,
            "major_id": r.major_id,
            "gender": r.gender,
            "total": r.total
        }
        for r in results
    ]

def stats_by_city(db: Session) -> list[dict]:
    """
    Thống kê số lượng sinh viên theo tỉnh/thành (city_id) theo từng năm và từng ngành.
    """
    results = (
        db.query(
            AdmittedStudent.year,
            AdmittedStudent.major_id,
            AdmittedStudent.city_id,
            func.count(AdmittedStudent.id).label("total")
        )
        .group_by(AdmittedStudent.year, AdmittedStudent.major_id, AdmittedStudent.city_id)
        .order_by(AdmittedStudent.major_id)
        .all()
    )
    return [
        {
            "year": r.year,
            "major_id": r.major_id,
            "city_id": r.city_id,
            "total": r.total
        }
        for r in results
    ]

def stats_by_admission_method(db: Session) -> list[dict]:
    """
    Thống kê số lượng sinh viên theo phương thức tuyển sinh (admission_method_id)
    theo từng năm và từng ngành.
    """
    results = (
        db.query(
            AdmittedStudent.year,
            AdmittedStudent.major_id,
            AdmittedStudent.admission_method_id,
            func.count(AdmittedStudent.id).label("total")
        )
        .group_by(AdmittedStudent.year, AdmittedStudent.major_id, AdmittedStudent.admission_method_id)
        .order_by(AdmittedStudent.major_id)
        .all()
    )
    return [
        {
            "year": r.year,
            "major_id": r.major_id,
            "admission_method_id": r.admission_method_id,
            "total": r.total
        }
        for r in results
    ]

def stats_by_score_range(db: Session) -> list[dict]:
    """
    Thống kê số lượng sinh viên theo khoảng điểm (total_score):
    Nhóm theo các khoảng: 15-16, 16-17, …, 29-30.
    Chỉ tính các sinh viên có total_score từ 15 đến thấp hơn 30,
    và sắp xếp theo major_id.
    """
    results = (
        db.query(
            AdmittedStudent.year,
            AdmittedStudent.major_id,
            func.floor(AdmittedStudent.total_score).label("score_bucket"),
            func.count(AdmittedStudent.id).label("total")
        )
        .filter(
            AdmittedStudent.total_score != None,
            AdmittedStudent.total_score >= 15,
            AdmittedStudent.total_score < 30
        )
        .group_by(AdmittedStudent.year, AdmittedStudent.major_id, func.floor(AdmittedStudent.total_score))
        .order_by(AdmittedStudent.major_id)
        .all()
    )

    stats = []
    for r in results:
        bucket = int(r.score_bucket)
        score_range = f"{bucket}-{bucket+1}"
        stats.append({
            "year": r.year,
            "major_id": r.major_id,
            "score_range": score_range,
            "total": r.total
        })
    return stats