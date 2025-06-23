import pytest
from sqlalchemy.orm import Session
from app.services.university_education_service import (
    create_course, get_course, get_courses, update_course, delete_course,
    create_major_course, get_major_course, get_major_courses, update_major_course, delete_major_course,
    create_major_course_detail, get_major_course_detail, get_major_course_details, update_major_course_detail, delete_major_course_detail
)
from app.schemas.university import (
    CourseCreate, CourseUpdate,
    MajorCourseCreate, MajorCourseUpdate,
    MajorCourseDetailCreate, MajorCourseDetailUpdate
)
from app.models.university import Course, MajorCourse, MajorCourseDetail, Faculty, Major
from app.core.exceptions import NotFoundException, AlreadyExistsException

@pytest.fixture
def test_faculty(db: Session):
    """Create a test faculty"""
    faculty = Faculty(
        name="Test Faculty for Education",
        description="Faculty for education testing",
        faculty_code="TFE"
    )
    db.add(faculty)
    db.commit()
    db.refresh(faculty)
    return faculty

@pytest.fixture
def test_major(db: Session, test_faculty):
    """Create a test major"""
    major = Major(
        faculty_id=test_faculty.id,
        major_code="TME",
        name="Test Major for Education",
        seats=100,
        description="Major for education testing"
    )
    db.add(major)
    db.commit()
    db.refresh(major)
    return major

@pytest.fixture
def test_course(db: Session):
    """Create a test course"""
    course_data = CourseCreate(
        course_code="CSE101",
        name="Introduction to Computer Science",
        credits=3.0
    )
    return create_course(db, course_data)

@pytest.fixture
def test_major_course(db: Session, test_major):
    """Create a test major course"""
    major_course_data = MajorCourseCreate(
        major_id=test_major.id,
        year=2025,
        type="Bachelor"
    )
    return create_major_course(db, major_course_data)

@pytest.fixture
def test_major_course_detail(db: Session, test_major_course, test_course):
    """Create a test major course detail"""
    major_course_detail_data = MajorCourseDetailCreate(
        major_course_id=test_major_course.id,
        course_id=test_course.id,
        semester=1,
        elective_course=False,
        pre_capstone=False,
        mandatory_capstone=False
    )
    return create_major_course_detail(db, major_course_detail_data)

def test_create_course(db: Session):
    """Test creating a course"""
    course_data = CourseCreate(
        course_code="MAT101",
        name="Mathematics I",
        credits=4.0
    )
    
    course = create_course(db, course_data)
    
    assert course.course_code == course_data.course_code
    assert course.name == course_data.name
    assert course.credits == course_data.credits
    
    # Test creating with existing course code
    with pytest.raises(AlreadyExistsException):
        create_course(db, course_data)

def test_get_course(db: Session, test_course):
    """Test retrieving course by ID"""
    course = get_course(db, test_course.id)
    
    assert course.id == test_course.id
    assert course.course_code == test_course.course_code
    assert course.name == test_course.name
    assert course.credits == test_course.credits
    
    # Test with non-existent ID
    with pytest.raises(NotFoundException):
        get_course(db, 99999)

def test_get_courses(db: Session, test_course):
    """Test retrieving all courses"""
    # Create additional course for testing
    course_data = CourseCreate(
        course_code="PHY101",
        name="Physics I",
        credits=4.0
    )
    create_course(db, course_data)
    
    courses = get_courses(db)
    
    assert len(courses) >= 2
    course_codes = [c.course_code for c in courses]
    assert test_course.course_code in course_codes
    assert "PHY101" in course_codes

def test_update_course(db: Session, test_course):
    """Test updating a course"""
    update_data = CourseUpdate(
        name="Updated Course Name",
        credits=3.5
    )
    
    updated_course = update_course(db, test_course.id, update_data)
    
    assert updated_course.id == test_course.id
    assert updated_course.name == update_data.name
    assert updated_course.credits == update_data.credits
    assert updated_course.course_code == test_course.course_code  # Unchanged
    
    # Test with non-existent ID
    with pytest.raises(NotFoundException):
        update_course(db, 99999, update_data)

def test_delete_course(db: Session):
    """Test deleting a course"""
    # Create a course to delete
    course_data = CourseCreate(
        course_code="DEL101",
        name="Course to Delete",
        credits=2.0
    )
    course = create_course(db, course_data)
    
    # Delete the course
    deleted_course = delete_course(db, course.id)
    
    assert deleted_course.id == course.id
    assert deleted_course.course_code == course.course_code
    
    # Verify course no longer exists
    with pytest.raises(NotFoundException):
        get_course(db, course.id)
    
    # Test with non-existent ID
    with pytest.raises(NotFoundException):
        delete_course(db, 99999)

def test_create_major_course(db: Session, test_major):
    """Test creating a major course"""
    major_course_data = MajorCourseCreate(
        major_id=test_major.id,
        year=2024,
        type="Master"
    )
    
    major_course = create_major_course(db, major_course_data)
    
    assert major_course.major_id == major_course_data.major_id
    assert major_course.year == major_course_data.year
    assert major_course.type == major_course_data.type
    
    # Test creating with existing major_id, year and type
    with pytest.raises(AlreadyExistsException):
        create_major_course(db, major_course_data)

def test_get_major_course(db: Session, test_major_course):
    """Test retrieving major course by ID"""
    major_course = get_major_course(db, test_major_course.id)
    
    assert major_course.id == test_major_course.id
    assert major_course.major_id == test_major_course.major_id
    assert major_course.year == test_major_course.year
    assert major_course.type == test_major_course.type
    
    # Test with non-existent ID
    with pytest.raises(NotFoundException):
        get_major_course(db, 99999)

def test_get_major_courses(db: Session, test_major_course, test_major):
    """Test retrieving all major courses"""
    # Create additional major course for testing
    major_course_data = MajorCourseCreate(
        major_id=test_major.id,
        year=2023,
        type="Bachelor"
    )
    create_major_course(db, major_course_data)
    
    major_courses = get_major_courses(db)
    
    assert len(major_courses) >= 2
    # Verify our test major courses are in the results
    found_test_course = False
    found_additional_course = False
    for mc in major_courses:
        if mc.id == test_major_course.id:
            found_test_course = True
        elif mc.major_id == test_major.id and mc.year == 2023:
            found_additional_course = True
    
    assert found_test_course
    assert found_additional_course

def test_update_major_course(db: Session, test_major_course):
    """Test updating a major course"""
    update_data = MajorCourseUpdate(
        year=2026,
        type="Updated Type"
    )
    
    updated_major_course = update_major_course(db, test_major_course.id, update_data)
    
    assert updated_major_course.id == test_major_course.id
    assert updated_major_course.year == update_data.year
    assert updated_major_course.type == update_data.type
    assert updated_major_course.major_id == test_major_course.major_id  # Unchanged
    
    # Test with non-existent ID
    with pytest.raises(NotFoundException):
        update_major_course(db, 99999, update_data)

def test_delete_major_course(db: Session, test_major):
    """Test deleting a major course"""
    # Create a major course to delete
    major_course_data = MajorCourseCreate(
        major_id=test_major.id,
        year=2022,
        type="Course to Delete"
    )
    major_course = create_major_course(db, major_course_data)
    
    # Delete the major course
    deleted_major_course = delete_major_course(db, major_course.id)
    
    assert deleted_major_course.id == major_course.id
    assert deleted_major_course.major_id == major_course.major_id
    
    # Verify major course no longer exists
    with pytest.raises(NotFoundException):
        get_major_course(db, major_course.id)
    
    # Test with non-existent ID
    with pytest.raises(NotFoundException):
        delete_major_course(db, 99999)

def test_create_major_course_detail(db: Session, test_major_course, test_course):
    """Test creating a major course detail"""
    major_course_detail_data = MajorCourseDetailCreate(
        major_course_id=test_major_course.id,
        course_id=test_course.id,
        semester=2,
        elective_course=True,
        pre_capstone=True,
        mandatory_capstone=False
    )
    
    major_course_detail = create_major_course_detail(db, major_course_detail_data)
    
    assert major_course_detail.major_course_id == major_course_detail_data.major_course_id
    assert major_course_detail.course_id == major_course_detail_data.course_id
    assert major_course_detail.semester == major_course_detail_data.semester
    assert major_course_detail.elective_course == major_course_detail_data.elective_course
    assert major_course_detail.pre_capstone == major_course_detail_data.pre_capstone
    assert major_course_detail.mandatory_capstone == major_course_detail_data.mandatory_capstone
    
    # Test creating with existing major_course_id, course_id and semester
    with pytest.raises(AlreadyExistsException):
        create_major_course_detail(db, major_course_detail_data)

def test_get_major_course_detail(db: Session, test_major_course_detail):
    """Test retrieving major course detail by ID"""
    major_course_detail = get_major_course_detail(db, test_major_course_detail.id)
    
    assert major_course_detail.id == test_major_course_detail.id
    assert major_course_detail.major_course_id == test_major_course_detail.major_course_id
    assert major_course_detail.course_id == test_major_course_detail.course_id
    assert major_course_detail.semester == test_major_course_detail.semester
    
    # Test with non-existent ID
    with pytest.raises(NotFoundException):
        get_major_course_detail(db, 99999)

def test_get_major_course_details(db: Session, test_major_course_detail, test_major_course, test_course):
    """Test retrieving all major course details"""
    # Create additional course for second detail
    course_data = CourseCreate(
        course_code="CSE102",
        name="Data Structures",
        credits=4.0
    )
    second_course = create_course(db, course_data)
    
    # Create additional major course detail for testing
    major_course_detail_data = MajorCourseDetailCreate(
        major_course_id=test_major_course.id,
        course_id=second_course.id,
        semester=2,
        elective_course=False,
        pre_capstone=False,
        mandatory_capstone=True
    )
    create_major_course_detail(db, major_course_detail_data)
    
    major_course_details = get_major_course_details(db)
    
    assert len(major_course_details) >= 2
    # Check if our test detail is in the list
    detail_ids = [detail.id for detail in major_course_details]
    assert test_major_course_detail.id in detail_ids

def test_update_major_course_detail(db: Session, test_major_course_detail):
    """Test updating a major course detail"""
    update_data = MajorCourseDetailUpdate(
        semester=3,
        elective_course=True,
        pre_capstone=True,
        mandatory_capstone=True
    )
    
    updated_detail = update_major_course_detail(db, test_major_course_detail.id, update_data)
    
    assert updated_detail.id == test_major_course_detail.id
    assert updated_detail.semester == update_data.semester
    assert updated_detail.elective_course == update_data.elective_course
    assert updated_detail.pre_capstone == update_data.pre_capstone
    assert updated_detail.mandatory_capstone == update_data.mandatory_capstone
    assert updated_detail.major_course_id == test_major_course_detail.major_course_id  # Unchanged
    assert updated_detail.course_id == test_major_course_detail.course_id  # Unchanged
    
    # Test with non-existent ID
    with pytest.raises(NotFoundException):
        update_major_course_detail(db, 99999, update_data)

def test_delete_major_course_detail(db: Session, test_major_course, test_course):
    """Test deleting a major course detail"""
    # Create a major course detail to delete
    detail_data = MajorCourseDetailCreate(
        major_course_id=test_major_course.id,
        course_id=test_course.id,
        semester=4,
        elective_course=False,
        pre_capstone=False,
        mandatory_capstone=False
    )
    detail = create_major_course_detail(db, detail_data)
    
    # Delete the major course detail
    deleted_detail = delete_major_course_detail(db, detail.id)
    
    assert deleted_detail.id == detail.id
    assert deleted_detail.major_course_id == detail.major_course_id
    
    # Verify detail no longer exists
    with pytest.raises(NotFoundException):
        get_major_course_detail(db, detail.id)
    
    # Test with non-existent ID
    with pytest.raises(NotFoundException):
        delete_major_course_detail(db, 99999)