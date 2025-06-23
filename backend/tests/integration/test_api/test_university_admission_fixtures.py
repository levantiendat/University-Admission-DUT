import pytest
from sqlalchemy.orm import Session
from app.models.university import (
    Faculty, Major, AdmissionMethod
)

@pytest.fixture
def create_test_faculty(db: Session):
    """Create a test faculty in the database"""
    faculty = Faculty(
        name="Test Faculty API",
        description="Test Faculty for API Testing",
        faculty_code="TFA"
    )
    db.add(faculty)
    db.commit()
    db.refresh(faculty)
    return faculty

@pytest.fixture
def create_test_major(db: Session, create_test_faculty):
    """Create a test major in the database"""
    major = Major(
        faculty_id=create_test_faculty.id,
        major_code="TMA",
        name="Test Major API",
        seats=100,
        description="Test Major for API Testing"
    )
    db.add(major)
    db.commit()
    db.refresh(major)
    return major

@pytest.fixture
def create_test_admission_method(db: Session):
    """Create a test admission method in the database"""
    admission_method = AdmissionMethod(
        name="Test Admission Method API",
        description="Test Admission Method for API Testing",
        min_score=0.0,
        max_score=30.0
    )
    db.add(admission_method)
    db.commit()
    db.refresh(admission_method)
    return admission_method