import pytest
from sqlalchemy.orm import Session
from app.models.university import (
    Faculty, Major, AdmissionMethod, AdmissionMethodMajor,
    Subject, SubjectScoreMethodGroup, SubjectGroupDetail
)

@pytest.fixture
def create_faculty(db: Session):
    """Create a faculty for testing"""
    faculty = Faculty(
        name="Test Faculty",
        description="Test Faculty Description",
        faculty_code="TF"
    )
    db.add(faculty)
    db.commit()
    db.refresh(faculty)
    return faculty

@pytest.fixture
def create_major(db: Session, create_faculty):
    """Create a major for testing"""
    major = Major(
        faculty_id=create_faculty.id,
        major_code="MAJOR01",
        name="Test Major",
        seats=100,
        description="Test Major Description"
    )
    db.add(major)
    db.commit()
    db.refresh(major)
    return major

@pytest.fixture
def create_admission_method(db: Session):
    """Create an admission method for testing"""
    admission_method = AdmissionMethod(
        name="Test Admission Method",
        description="Test Admission Method Description",
        min_score=0.0,
        max_score=30.0
    )
    db.add(admission_method)
    db.commit()
    db.refresh(admission_method)
    return admission_method

@pytest.fixture
def create_admission_method_major(db: Session, create_major, create_admission_method):
    """Create an admission method major for testing"""
    admission_method_major = AdmissionMethodMajor(
        major_id=create_major.id,
        admission_methods_id=create_admission_method.id
    )
    db.add(admission_method_major)
    db.commit()
    db.refresh(admission_method_major)
    return admission_method_major

@pytest.fixture
def create_subjects(db: Session):
    """Create subjects for testing"""
    subjects = []
    for i, name in enumerate(["Mathematics", "Literature", "Physics", "Chemistry", "Biology"]):
        subject = Subject(name=name)
        db.add(subject)
        db.commit()
        db.refresh(subject)
        subjects.append(subject)
    return subjects

@pytest.fixture
def create_subject_group(db: Session):
    """Create a subject group for testing"""
    subject_group = SubjectScoreMethodGroup(name="A00")
    db.add(subject_group)
    db.commit()
    db.refresh(subject_group)
    return subject_group

@pytest.fixture
def create_subject_group_details(db: Session, create_subjects, create_subject_group):
    """Create subject group details for testing"""
    details = []
    for i, subject in enumerate(create_subjects[:3]):  # Use first 3 subjects
        detail = SubjectGroupDetail(
            group_id=create_subject_group.id,
            subject_id=subject.id,
            coefficient=1.0
        )
        db.add(detail)
        db.commit()
        db.refresh(detail)
        details.append(detail)
    return details