from app.models.university import Faculty, Major, AdmissionMethod, AdmissionMethodMajor
from app.models.university import Subject, SubjectScoreMethodGroup, SubjectGroupDetail, ConvertPoint, PreviousAdmission
from app.models.university import Course, MajorCourse, MajorCourseDetail, CoursePriorCourse, CoursePrerequisite, CourseCorequisite
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, AlreadyExistsException
from app.core.exceptions import ForbiddenException

from app.schemas.university import FacultyCreate, FacultyUpdate, MajorCreate, MajorUpdate, AdmissionMethodCreate, AdmissionMethodUpdate
from app.schemas.university import AdmissionMethodMajorCreate, AdmissionMethodMajorUpdate, SubjectCreate, SubjectUpdate
from app.schemas.university import SubjectScoreMethodGroupCreate, SubjectScoreMethodGroupUpdate
from app.schemas.university import SubjectGroupDetailCreate, SubjectGroupDetailUpdate, ConvertPointCreate, ConvertPointUpdate
from app.schemas.university import PreviousAdmissionCreate, PreviousAdmissionUpdate


def create_faculty(db: Session, faculty: FacultyCreate) -> Faculty:
    db_faculty = db.query(Faculty).filter(Faculty.name == faculty.name).first()
    if db_faculty:
        raise AlreadyExistsException("Faculty already exists")
    db_faculty = Faculty(**faculty.dict())
    db.add(db_faculty)
    db.commit()
    db.refresh(db_faculty)
    return db_faculty

def get_faculty(db: Session, faculty_id: int) -> Faculty:
    db_faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not db_faculty:
        raise NotFoundException("Faculty not found")
    return db_faculty

def get_faculties(db: Session, skip: int = 0, limit: int = 100) -> list[Faculty]:
    return db.query(Faculty).offset(skip).limit(limit).all()

def update_faculty(db: Session, faculty_id: int, faculty: FacultyUpdate) -> Faculty:
    db_faculty = get_faculty(db, faculty_id)
    for key, value in faculty.dict(exclude_unset=True).items():
        setattr(db_faculty, key, value)
    db.commit()
    db.refresh(db_faculty)
    return db_faculty

def delete_faculty(db: Session, faculty_id: int) -> Faculty:
    db_faculty = get_faculty(db, faculty_id)
    db.delete(db_faculty)
    db.commit()
    return db_faculty

def create_major(db: Session, major: MajorCreate) -> Major:
    db_major = db.query(Major).filter(Major.name == major.name).first()
    if db_major:
        raise AlreadyExistsException("Major already exists")
    db_major = Major(**major.dict())
    db.add(db_major)
    db.commit()
    db.refresh(db_major)
    return db_major

def get_major(db: Session, major_id: int) -> Major:
    db_major = db.query(Major).filter(Major.id == major_id).first()
    if not db_major:
        raise NotFoundException("Major not found")
    return db_major

def get_majors(db: Session, skip: int = 0, limit: int = 100) -> list[Major]:
    return db.query(Major).offset(skip).limit(limit).all()

def update_major(db: Session, major_id: int, major: MajorUpdate) -> Major:
    db_major = get_major(db, major_id)
    for key, value in major.dict(exclude_unset=True).items():
        setattr(db_major, key, value)
    db.commit()
    db.refresh(db_major)
    return db_major

def delete_major(db: Session, major_id: int) -> Major:
    db_major = get_major(db, major_id)
    db.delete(db_major)
    db.commit()
    return db_major

def create_admission_method(db: Session, admission_method: AdmissionMethodCreate) -> AdmissionMethod:
    db_admission_method = db.query(AdmissionMethod).filter(AdmissionMethod.name == admission_method.name).first()
    if db_admission_method:
        raise AlreadyExistsException("Admission method already exists")
    db_admission_method = AdmissionMethod(**admission_method.dict())
    db.add(db_admission_method)
    db.commit()
    db.refresh(db_admission_method)
    return db_admission_method

def get_admission_method(db: Session, admission_method_id: int) -> AdmissionMethod:
    db_admission_method = db.query(AdmissionMethod).filter(AdmissionMethod.id == admission_method_id).first()
    if not db_admission_method:
        raise NotFoundException("Admission method not found")
    return db_admission_method

def get_admission_methods(db: Session, skip: int = 0, limit: int = 100) -> list[AdmissionMethod]:
    return db.query(AdmissionMethod).offset(skip).limit(limit).all()

def update_admission_method(db: Session, admission_method_id: int, admission_method: AdmissionMethodUpdate) -> AdmissionMethod:
    db_admission_method = get_admission_method(db, admission_method_id)
    for key, value in admission_method.dict(exclude_unset=True).items():
        setattr(db_admission_method, key, value)
    db.commit()
    db.refresh(db_admission_method)
    return db_admission_method

def delete_admission_method(db: Session, admission_method_id: int) -> AdmissionMethod:
    db_admission_method = get_admission_method(db, admission_method_id)
    db.delete(db_admission_method)
    db.commit()
    return db_admission_method

def create_admission_method_major(db: Session, admission_method_major: AdmissionMethodMajorCreate) -> AdmissionMethodMajor:
    db_admission_method_major = db.query(AdmissionMethodMajor).filter(
        AdmissionMethodMajor.major_id == admission_method_major.major_id,
        AdmissionMethodMajor.admission_methods_id == admission_method_major.admission_methods_id
    ).first()
    if db_admission_method_major:
        raise AlreadyExistsException("Admission method major already exists")
    db_admission_method_major = AdmissionMethodMajor(**admission_method_major.dict())
    db.add(db_admission_method_major)
    db.commit()
    db.refresh(db_admission_method_major)
    return db_admission_method_major

def get_admission_method_major(db: Session, admission_method_major_id: int) -> AdmissionMethodMajor:
    db_admission_method_major = db.query(AdmissionMethodMajor).filter(AdmissionMethodMajor.id == admission_method_major_id).first()
    if not db_admission_method_major:
        raise NotFoundException("Admission method major not found")
    return db_admission_method_major

def get_admission_method_majors(db: Session, skip: int = 0, limit: int = 100) -> list[AdmissionMethodMajor]:
    return db.query(AdmissionMethodMajor).offset(skip).limit(limit).all()

def update_admission_method_major(db: Session, admission_method_major_id: int, admission_method_major: AdmissionMethodMajorUpdate) -> AdmissionMethodMajor:
    db_admission_method_major = get_admission_method_major(db, admission_method_major_id)
    for key, value in admission_method_major.dict(exclude_unset=True).items():
        setattr(db_admission_method_major, key, value)
    db.commit()
    db.refresh(db_admission_method_major)
    return db_admission_method_major

def delete_admission_method_major(db: Session, admission_method_major_id: int) -> AdmissionMethodMajor:
    db_admission_method_major = get_admission_method_major(db, admission_method_major_id)
    db.delete(db_admission_method_major)
    db.commit()
    return db_admission_method_major

def create_subject(db: Session, subject: SubjectCreate) -> Subject:
    db_subject = db.query(Subject).filter(Subject.name == subject.name).first()
    if db_subject:
        raise AlreadyExistsException("Subject already exists")
    db_subject = Subject(**subject.dict())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

def get_subject(db: Session, subject_id: int) -> Subject:
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not db_subject:
        raise NotFoundException("Subject not found")
    return db_subject

def get_subjects(db: Session, skip: int = 0, limit: int = 100) -> list[Subject]:
    return db.query(Subject).offset(skip).limit(limit).all()

def update_subject(db: Session, subject_id: int, subject: SubjectUpdate) -> Subject:
    db_subject = get_subject(db, subject_id)
    for key, value in subject.dict(exclude_unset=True).items():
        setattr(db_subject, key, value)
    db.commit()
    db.refresh(db_subject)
    return db_subject

def delete_subject(db: Session, subject_id: int) -> Subject:
    db_subject = get_subject(db, subject_id)
    db.delete(db_subject)
    db.commit()
    return db_subject

def create_subject_score_method_group(db: Session, subject_score_method_group: SubjectScoreMethodGroupCreate) -> SubjectScoreMethodGroup:
    db_subject_score_method_group = db.query(SubjectScoreMethodGroup).filter(
        SubjectScoreMethodGroup.admission_method_major_id == subject_score_method_group.admission_method_major_id,
        SubjectScoreMethodGroup.name == subject_score_method_group.name
    ).first()
    if db_subject_score_method_group:
        raise AlreadyExistsException("Subject score method group already exists")
    db_subject_score_method_group = SubjectScoreMethodGroup(**subject_score_method_group.dict())
    db.add(db_subject_score_method_group)
    db.commit()
    db.refresh(db_subject_score_method_group)
    return db_subject_score_method_group

def get_subject_score_method_group(db: Session, subject_score_method_group_id: int) -> SubjectScoreMethodGroup:
    db_subject_score_method_group = db.query(SubjectScoreMethodGroup).filter(SubjectScoreMethodGroup.id == subject_score_method_group_id).first()
    if not db_subject_score_method_group:
        raise NotFoundException("Subject score method group not found")
    return db_subject_score_method_group

def get_subject_score_method_groups(db: Session, skip: int = 0, limit: int = 100) -> list[SubjectScoreMethodGroup]:
    return db.query(SubjectScoreMethodGroup).offset(skip).limit(limit).all()

def update_subject_score_method_group(db: Session, subject_score_method_group_id: int, subject_score_method_group: SubjectScoreMethodGroupUpdate) -> SubjectScoreMethodGroup:
    db_subject_score_method_group = get_subject_score_method_group(db, subject_score_method_group_id)
    for key, value in subject_score_method_group.dict(exclude_unset=True).items():
        setattr(db_subject_score_method_group, key, value)
    db.commit()
    db.refresh(db_subject_score_method_group)
    return db_subject_score_method_group

def delete_subject_score_method_group(db: Session, subject_score_method_group_id: int) -> SubjectScoreMethodGroup:
    db_subject_score_method_group = get_subject_score_method_group(db, subject_score_method_group_id)
    db.delete(db_subject_score_method_group)
    db.commit()
    return db_subject_score_method_group

def create_subject_group_detail(db: Session, subject_group_detail: SubjectGroupDetailCreate) -> SubjectGroupDetail:
    db_subject_group_detail = db.query(SubjectGroupDetail).filter(
        SubjectGroupDetail.group_id == subject_group_detail.group_id,
        SubjectGroupDetail.subject_id == subject_group_detail.subject_id
    ).first()
    if db_subject_group_detail:
        raise AlreadyExistsException("Subject group detail already exists")
    db_subject_group_detail = SubjectGroupDetail(**subject_group_detail.dict())
    db.add(db_subject_group_detail)
    db.commit()
    db.refresh(db_subject_group_detail)
    return db_subject_group_detail

def get_subject_group_detail(db: Session, subject_group_detail_id: int) -> SubjectGroupDetail:
    db_subject_group_detail = db.query(SubjectGroupDetail).filter(SubjectGroupDetail.id == subject_group_detail_id).first()
    if not db_subject_group_detail:
        raise NotFoundException("Subject group detail not found")
    return db_subject_group_detail

def get_subject_group_details(db: Session, skip: int = 0, limit: int = 100) -> list[SubjectGroupDetail]:
    return db.query(SubjectGroupDetail).offset(skip).limit(limit).all()

def update_subject_group_detail(db: Session, subject_group_detail_id: int, subject_group_detail: SubjectGroupDetailUpdate) -> SubjectGroupDetail:
    db_subject_group_detail = get_subject_group_detail(db, subject_group_detail_id)
    for key, value in subject_group_detail.dict(exclude_unset=True).items():
        setattr(db_subject_group_detail, key, value)
    db.commit()
    db.refresh(db_subject_group_detail)
    return db_subject_group_detail

def delete_subject_group_detail(db: Session, subject_group_detail_id: int) -> SubjectGroupDetail:
    db_subject_group_detail = get_subject_group_detail(db, subject_group_detail_id)
    db.delete(db_subject_group_detail)
    db.commit()
    return db_subject_group_detail

def create_convert_point(db: Session, convert_point: ConvertPointCreate) -> ConvertPoint:
    db_convert_point = db.query(ConvertPoint).filter(
        ConvertPoint.admission_methods_id == convert_point.admission_methods_id,
        ConvertPoint.origin_min == convert_point.origin_min,
        ConvertPoint.origin_max == convert_point.origin_max
    ).first()
    if db_convert_point:
        raise AlreadyExistsException("Convert point already exists")
    db_convert_point = ConvertPoint(**convert_point.dict())
    db.add(db_convert_point)
    db.commit()
    db.refresh(db_convert_point)
    return db_convert_point

def get_convert_point(db: Session, convert_point_id: int) -> ConvertPoint:
    db_convert_point = db.query(ConvertPoint).filter(ConvertPoint.id == convert_point_id).first()
    if not db_convert_point:
        raise NotFoundException("Convert point not found")
    return db_convert_point

def get_convert_points(db: Session, skip: int = 0, limit: int = 100) -> list[ConvertPoint]:
    return db.query(ConvertPoint).offset(skip).limit(limit).all()

def update_convert_point(db: Session, convert_point_id: int, convert_point: ConvertPointUpdate) -> ConvertPoint:
    db_convert_point = get_convert_point(db, convert_point_id)
    for key, value in convert_point.dict(exclude_unset=True).items():
        setattr(db_convert_point, key, value)
    db.commit()
    db.refresh(db_convert_point)
    return db_convert_point

def delete_convert_point(db: Session, convert_point_id: int) -> ConvertPoint:
    db_convert_point = get_convert_point(db, convert_point_id)
    db.delete(db_convert_point)
    db.commit()
    return db_convert_point

def create_previous_admission(db: Session, previous_admission: PreviousAdmissionCreate) -> PreviousAdmission:
    db_previous_admission = db.query(PreviousAdmission).filter(
        PreviousAdmission.major_id == previous_admission.major_id,
        PreviousAdmission.year == previous_admission.year,
        PreviousAdmission.admission_methods_id == previous_admission.admission_methods_id
    ).first()
    if db_previous_admission:
        raise AlreadyExistsException("Previous admission already exists")
    db_previous_admission = PreviousAdmission(**previous_admission.dict())
    db.add(db_previous_admission)
    db.commit()
    db.refresh(db_previous_admission)
    return db_previous_admission

def get_previous_admission(db: Session, previous_admission_id: int) -> PreviousAdmission:
    db_previous_admission = db.query(PreviousAdmission).filter(PreviousAdmission.id == previous_admission_id).first()
    if not db_previous_admission:
        raise NotFoundException("Previous admission not found")
    return db_previous_admission

def get_previous_admissions(db: Session, skip: int = 0, limit: int = 100) -> list[PreviousAdmission]:
    return db.query(PreviousAdmission).offset(skip).limit(limit).all()

def update_previous_admission(db: Session, previous_admission_id: int, previous_admission: PreviousAdmissionUpdate) -> PreviousAdmission:
    db_previous_admission = get_previous_admission(db, previous_admission_id)
    for key, value in previous_admission.dict(exclude_unset=True).items():
        setattr(db_previous_admission, key, value)
    db.commit()
    db.refresh(db_previous_admission)
    return db_previous_admission

def delete_previous_admission(db: Session, previous_admission_id: int) -> PreviousAdmission:
    db_previous_admission = get_previous_admission(db, previous_admission_id)
    db.delete(db_previous_admission)
    db.commit()
    return db_previous_admission

