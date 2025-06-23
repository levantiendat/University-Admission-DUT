import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.university import (
    Faculty, Major, Course, MajorCourse, MajorCourseDetail,
    CoursePriorCourse, CoursePrerequisite, CourseCorequisite
)

@pytest.fixture
def setup_education_test_data(db: Session):
    """Create test data for education tests"""
    # Create faculty
    faculty = Faculty(
        name="Computer Science Faculty",
        description="Faculty for Computer Science and IT",
        faculty_code="CSF"
    )
    db.add(faculty)
    db.commit()
    db.refresh(faculty)
    
    # Create major
    major = Major(
        faculty_id=faculty.id,
        major_code="CS",
        name="Computer Science",
        seats=100,
        description="Bachelor of Computer Science"
    )
    db.add(major)
    db.commit()
    db.refresh(major)
    
    # Create courses
    course1 = Course(
        course_code="CS101",
        name="Introduction to Programming",
        credits=3.0
    )
    course2 = Course(
        course_code="CS102",
        name="Data Structures",
        credits=4.0
    )
    course3 = Course(
        course_code="CS103",
        name="Database Systems",
        credits=3.0
    )
    
    db.add_all([course1, course2, course3])
    db.commit()
    db.refresh(course1)
    db.refresh(course2)
    db.refresh(course3)
    
    # Create major course
    major_course = MajorCourse(
        major_id=major.id,
        year=2024,
        type="Bachelor"
    )
    db.add(major_course)
    db.commit()
    db.refresh(major_course)
    
    # Create major course details
    detail1 = MajorCourseDetail(
        major_course_id=major_course.id,
        course_id=course1.id,
        semester=1,
        elective_course=False,
        pre_capstone=False,
        mandatory_capstone=False
    )
    detail2 = MajorCourseDetail(
        major_course_id=major_course.id,
        course_id=course2.id,
        semester=2,
        elective_course=False,
        pre_capstone=False,
        mandatory_capstone=False
    )
    detail3 = MajorCourseDetail(
        major_course_id=major_course.id,
        course_id=course3.id,
        semester=3,
        elective_course=True,
        pre_capstone=False,
        mandatory_capstone=False
    )
    
    db.add_all([detail1, detail2, detail3])
    db.commit()
    
    # Create course relationships
    # Data Structures requires Intro to Programming
    prereq = CoursePrerequisite(
        major_course_detail_id=detail2.id,
        prerequisite_major_course_detail_id=detail1.id
    )
    
    # Database Systems should be taken after Intro to Programming
    prior = CoursePriorCourse(
        major_course_detail_id=detail3.id,
        prior_course_detail_id=detail1.id
    )
    
    db.add_all([prereq, prior])
    db.commit()
    
    return {
        "faculty": faculty,
        "major": major,
        "courses": [course1, course2, course3],
        "major_course": major_course,
        "details": [detail1, detail2, detail3]
    }

def test_get_courses(client: TestClient, setup_education_test_data):
    """Test getting all courses endpoint"""
    response = client.get("/api/university-educations/courses")
    
    assert response.status_code == 200
    courses = response.json()
    assert isinstance(courses, list)
    assert len(courses) >= 3
    
    # Verify our test courses are in the returned data
    course_codes = [c["course_code"] for c in courses]
    assert "CS101" in course_codes
    assert "CS102" in course_codes
    assert "CS103" in course_codes

def test_create_course(client: TestClient, admin_token_headers, user_token_headers):
    """Test creating a course endpoint"""
    course_data = {
        "course_code": "MATH101",
        "name": "Calculus I",
        "credits": 4.0
    }
    
    # Test without token (should fail)
    response = client.post("/api/university-educations/courses", json=course_data)
    assert response.status_code == 401
    
    # Test with user token (should fail - not admin)
    response = client.post(
        "/api/university-educations/courses",
        json=course_data,
        headers=user_token_headers
    )
    assert response.status_code == 403
    
    # Test with admin token (should succeed)
    response = client.post(
        "/api/university-educations/courses",
        json=course_data,
        headers=admin_token_headers
    )
    assert response.status_code == 201
    created_course = response.json()
    assert created_course["course_code"] == course_data["course_code"]
    assert created_course["name"] == course_data["name"]
    assert created_course["credits"] == course_data["credits"]

def test_get_course_by_id(client: TestClient, setup_education_test_data):
    """Test getting a course by ID"""
    course_id = setup_education_test_data["courses"][0].id
    
    response = client.get(f"/api/university-educations/courses/{course_id}")
    
    assert response.status_code == 200
    course = response.json()
    assert course["id"] == course_id
    assert course["course_code"] == "CS101"
    assert course["name"] == "Introduction to Programming"
    
    # Test non-existent course ID
    response = client.get("/api/university-educations/courses/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_update_course(client: TestClient, setup_education_test_data, admin_token_headers):
    """Test updating a course"""
    course_id = setup_education_test_data["courses"][1].id
    
    update_data = {
        "name": "Advanced Data Structures",
        "credits": 4.5
    }
    
    response = client.put(
        f"/api/university-educations/courses/{course_id}",
        json=update_data,
        headers=admin_token_headers
    )
    
    assert response.status_code == 200
    updated = response.json()
    assert updated["id"] == course_id
    assert updated["name"] == update_data["name"]
    assert updated["credits"] == update_data["credits"]
    assert updated["course_code"] == "CS102"  # Unchanged

def test_create_major_course(client: TestClient, setup_education_test_data, admin_token_headers):
    """Test creating a major course"""
    major_id = setup_education_test_data["major"].id
    
    major_course_data = {
        "major_id": major_id,
        "year": 2025,
        "type": "Master"
    }
    
    response = client.post(
        "/api/university-educations/major_courses",
        json=major_course_data,
        headers=admin_token_headers
    )
    
    assert response.status_code == 201
    created = response.json()
    assert created["major_id"] == major_id
    assert created["year"] == 2025
    assert created["type"] == "Master"

def test_get_major_courses(client: TestClient, setup_education_test_data):
    """Test getting all major courses"""
    response = client.get("/api/university-educations/major_courses")
    
    assert response.status_code == 200
    major_courses = response.json()
    assert isinstance(major_courses, list)
    assert len(major_courses) >= 1
    
    # Check for our specific test data
    test_mc = setup_education_test_data["major_course"]
    found = False
    for mc in major_courses:
        if mc["id"] == test_mc.id:
            found = True
            assert mc["major_id"] == test_mc.major_id
            assert mc["year"] == test_mc.year
            assert mc["type"] == test_mc.type
    
    assert found, "Test major course not found in results"

def test_get_major_course_by_id(client: TestClient, setup_education_test_data):
    """Test getting a major course by ID"""
    major_course_id = setup_education_test_data["major_course"].id
    
    response = client.get(f"/api/university-educations/major_courses/{major_course_id}")
    
    assert response.status_code == 200
    major_course = response.json()
    assert major_course["id"] == major_course_id
    assert major_course["major_id"] == setup_education_test_data["major"].id
    assert major_course["year"] == 2024
    assert major_course["type"] == "Bachelor"

def test_create_major_course_detail(client: TestClient, setup_education_test_data, admin_token_headers):
    """Test creating a major course detail"""
    major_course_id = setup_education_test_data["major_course"].id
    course_id = setup_education_test_data["courses"][2].id
    
    detail_data = {
        "major_course_id": major_course_id,
        "course_id": course_id,
        "semester": 4,
        "elective_course": True,
        "pre_capstone": True,
        "mandatory_capstone": False
    }
    
    response = client.post(
        "/api/university-educations/major_course_details",
        json=detail_data,
        headers=admin_token_headers
    )
    
    assert response.status_code == 201
    created = response.json()
    assert created["major_course_id"] == major_course_id
    assert created["course_id"] == course_id
    assert created["semester"] == 4
    assert created["elective_course"] == True
    assert created["pre_capstone"] == True
    assert created["mandatory_capstone"] == False

def test_get_major_course_details(client: TestClient, setup_education_test_data):
    """Test getting all major course details"""
    response = client.get("/api/university-educations/major_course_details")
    
    assert response.status_code == 200
    details = response.json()
    assert isinstance(details, list)
    assert len(details) >= 3  # We created 3 in the fixture
    
    # Check for specific semester values we created
    semesters = [d["semester"] for d in details]
    assert 1 in semesters
    assert 2 in semesters
    assert 3 in semesters

def test_get_major_course_details_by_major_course_id(client: TestClient, setup_education_test_data):
    """Test getting major course details by major course ID"""
    major_course_id = setup_education_test_data["major_course"].id
    
    response = client.get(f"/api/university-educations/major_course_details_by_major_course_id?major_course_id={major_course_id}")
    
    assert response.status_code == 200
    result = response.json()
    
    # Check for expected sections
    assert "courses" in result
    assert "major_course_details" in result
    
    # Verify we have our 3 courses and details
    assert len(result["courses"]) >= 3
    assert len(result["major_course_details"]) >= 3
    
    # Check for course relationships
    for detail in result["major_course_details"]:
        assert "id" in detail
        assert "course_id" in detail
        assert "semester" in detail
        assert "prior_courses" in detail
        assert "prerequisites" in detail
        assert "corequisites" in detail

def test_create_course_prerequisite(client: TestClient, setup_education_test_data, admin_token_headers):
    """Test creating a course prerequisite relationship"""
    detail1 = setup_education_test_data["details"][0].id  # CS101
    detail3 = setup_education_test_data["details"][2].id  # CS103
    
    prereq_data = {
        "major_course_detail_id": detail3,
        "prerequisite_major_course_detail_id": detail1
    }
    
    response = client.post(
        "/api/university-educations/course_prerequisites",
        json=prereq_data,
        headers=admin_token_headers
    )
    
    assert response.status_code == 201
    created = response.json()
    assert created["major_course_detail_id"] == detail3
    assert created["prerequisite_major_course_detail_id"] == detail1

def test_create_course_corequisite(client: TestClient, setup_education_test_data, admin_token_headers):
    """Test creating a course corequisite relationship"""
    detail2 = setup_education_test_data["details"][1].id  # CS102
    detail3 = setup_education_test_data["details"][2].id  # CS103
    
    coreq_data = {
        "major_course_detail_id": detail3,
        "corequisite_major_course_detail_id": detail2
    }
    
    response = client.post(
        "/api/university-educations/course_corequisites",
        json=coreq_data,
        headers=admin_token_headers
    )
    
    assert response.status_code == 201
    created = response.json()
    assert created["major_course_detail_id"] == detail3
    assert created["corequisite_major_course_detail_id"] == detail2