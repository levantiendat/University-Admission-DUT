import pytest
from sqlalchemy.orm import Session
from app.services.university_admission_service import (
    create_faculty, get_faculty, get_faculties, update_faculty, delete_faculty,
    create_major, get_major, get_majors, update_major, delete_major,
    create_admission_method, get_admission_method, get_admission_methods,
    create_admission_method_major, get_admission_method_major, get_admission_method_majors,
    calculate_admission_scores
)
from app.schemas.university import (
    FacultyCreate, FacultyUpdate,
    MajorCreate, MajorUpdate,
    AdmissionMethodCreate, AdmissionMethodUpdate,
    AdmissionMethodMajorCreate
)
from app.core.exceptions import AlreadyExistsException, NotFoundException

# Import fixtures
from .test_university_admission_fixtures import (
    create_faculty, create_major, create_admission_method,
    create_admission_method_major, create_subjects, create_subject_group,
    create_subject_group_details
)

def test_create_faculty(db: Session):
    from app.schemas.university import FacultyCreate
    from app.services.university_admission_service import create_faculty as create_faculty_service
    
    faculty_data = FacultyCreate(
        name="Test Faculty",
        description="Test Faculty Description",
        faculty_code="TFE"
    )
    
    created_faculty = create_faculty_service(db, faculty_data)
    assert created_faculty.name == faculty_data.name
    assert created_faculty.description == faculty_data.description
    assert created_faculty.faculty_code == faculty_data.faculty_code

def test_get_faculty(db: Session, create_faculty):
    """Test getting a faculty"""
    # Test lấy faculty theo ID
    faculty = get_faculty(db, create_faculty.id)
    assert faculty.id == create_faculty.id
    assert faculty.name == create_faculty.name
    
    # Test lấy faculty với ID không tồn tại
    with pytest.raises(NotFoundException) as excinfo:
        get_faculty(db, 999999)
    assert "Faculty not found" in str(excinfo.value)

def test_get_faculties(db: Session):
    from app.services.university_admission_service import get_faculties as get_faculties_service
    from app.models.university import Faculty
    
    # Tạo một vài faculties để test
    faculty1 = Faculty(name="Test Faculty 1", description="Description 1", faculty_code="TF1")
    faculty2 = Faculty(name="Test Faculty 2", description="Description 2", faculty_code="TF2")
    db.add_all([faculty1, faculty2])
    db.commit()
    
    # Test get_faculties service
    faculties = get_faculties_service(db)
    assert len(faculties) >= 2
    faculty_names = [f.name for f in faculties]
    assert "Test Faculty 1" in faculty_names
    assert "Test Faculty 2" in faculty_names

def test_update_faculty(db: Session, create_faculty):
    """Test updating a faculty"""
    # Test cập nhật faculty
    faculty_update = FacultyUpdate(
        name="Updated Faculty",
        description="Updated Faculty Description",
        faculty_code="UF"
    )
    
    updated_faculty = update_faculty(db, create_faculty.id, faculty_update)
    
    assert updated_faculty.id == create_faculty.id
    assert updated_faculty.name == "Updated Faculty"
    assert updated_faculty.description == "Updated Faculty Description"
    assert updated_faculty.faculty_code == "UF"
    
    # Test cập nhật một số trường
    partial_update = FacultyUpdate(description="Partially Updated Description")
    updated_faculty = update_faculty(db, create_faculty.id, partial_update)
    
    assert updated_faculty.name == "Updated Faculty"  # Không đổi
    assert updated_faculty.description == "Partially Updated Description"
    assert updated_faculty.faculty_code == "UF"  # Không đổi
    
    # Test cập nhật với ID không tồn tại
    with pytest.raises(NotFoundException) as excinfo:
        update_faculty(db, 999999, faculty_update)
    assert "Faculty not found" in str(excinfo.value)

def test_delete_faculty(db: Session):
    from app.services.university_admission_service import delete_faculty as delete_faculty_service
    from app.models.university import Faculty
    
    # Tạo faculty để xóa
    faculty_to_delete = Faculty(name="Delete Me", description="Delete Description", faculty_code="DEL")
    db.add(faculty_to_delete)
    db.commit()
    db.refresh(faculty_to_delete)
    
    # Test delete_faculty service
    deleted = delete_faculty_service(db, faculty_to_delete.id)
    assert deleted.id == faculty_to_delete.id
    assert deleted.name == "Delete Me"
    
    # Kiểm tra faculty đã bị xóa
    assert db.query(Faculty).filter(Faculty.id == faculty_to_delete.id).first() is None

def test_create_major(db: Session, create_faculty):
    """Test creating a major"""
    from app.services.university_admission_service import create_major as create_major_service
    
    # Test tạo major mới
    major_data = MajorCreate(
        faculty_id=create_faculty.id,
        major_code="MAJOR01",
        name="Computer Science",
        seats=100,
        description="Major of Computer Science"
    )
    
    major = create_major_service(db, major_data)
    
    assert major.name == "Computer Science"
    assert major.major_code == "MAJOR01"
    assert major.faculty_id == create_faculty.id
    assert major.seats == 100
    assert major.description == "Major of Computer Science"
    
    # Test tạo major với tên đã tồn tại
    with pytest.raises(AlreadyExistsException) as excinfo:
        create_major_service(db, major_data)
    assert "Major already exists" in str(excinfo.value)

def test_get_major(db: Session, create_major):
    """Test getting a major"""
    # Test lấy major theo ID
    major = get_major(db, create_major.id)
    assert major.id == create_major.id
    assert major.name == create_major.name
    
    # Test lấy major với ID không tồn tại
    with pytest.raises(NotFoundException) as excinfo:
        get_major(db, 999999)
    assert "Major not found" in str(excinfo.value)

def test_get_majors(db: Session, create_major, create_faculty):
    """Test getting all majors"""
    # Use the imported service function, not the fixture
    from app.services.university_admission_service import create_major as create_major_service
    
    # Tạo thêm một major
    major_data = MajorCreate(
        faculty_id=create_faculty.id,
        major_code="MAJOR02",
        name="Information Technology",
        seats=120,
        description="Major of Information Technology"
    )
    create_major_service(db, major_data)
    
    # Test lấy danh sách major
    majors = get_majors(db)
    assert len(majors) >= 2
    major_names = [m.name for m in majors]
    assert "Test Major" in major_names
    assert "Information Technology" in major_names

def test_update_major(db: Session, create_major):
    """Test updating a major"""
    # Test cập nhật major
    major_update = MajorUpdate(
        name="Updated Major",
        major_code="UMAJOR",
        seats=150,
        description="Updated Major Description"
    )
    
    updated_major = update_major(db, create_major.id, major_update)
    
    assert updated_major.id == create_major.id
    assert updated_major.name == "Updated Major"
    assert updated_major.major_code == "UMAJOR"
    assert updated_major.seats == 150
    assert updated_major.description == "Updated Major Description"
    
    # Test cập nhật một số trường
    partial_update = MajorUpdate(seats=200)
    updated_major = update_major(db, create_major.id, partial_update)
    
    assert updated_major.name == "Updated Major"  # Không đổi
    assert updated_major.seats == 200
    assert updated_major.description == "Updated Major Description"  # Không đổi
    
    # Test cập nhật với ID không tồn tại
    with pytest.raises(NotFoundException) as excinfo:
        update_major(db, 999999, major_update)
    assert "Major not found" in str(excinfo.value)

def test_delete_major(db: Session, create_faculty):
    """Test deleting a major"""
    from app.services.university_admission_service import create_major as create_major_service
    
    # Tạo major để xóa
    major_data = MajorCreate(
        faculty_id=create_faculty.id,
        major_code="MAJORDEL",
        name="Major To Delete",
        seats=100,
        description="Major To Delete Description"
    )
    major = create_major_service(db, major_data)
    
    # Test xóa major
    deleted_major = delete_major(db, major.id)
    assert deleted_major.id == major.id
    assert deleted_major.name == "Major To Delete"
    
    # Kiểm tra major đã bị xóa
    with pytest.raises(NotFoundException) as excinfo:
        get_major(db, major.id)
    assert "Major not found" in str(excinfo.value)
    
    # Test xóa với ID không tồn tại
    with pytest.raises(NotFoundException) as excinfo:
        delete_major(db, 999999)
    assert "Major not found" in str(excinfo.value)

def test_create_admission_method(db: Session):
    """Test creating an admission method"""
    # Use the imported service function with an alias to avoid confusion with the fixture
    from app.services.university_admission_service import create_admission_method as create_admission_method_service
    
    # Test tạo admission method mới
    admission_method_data = AdmissionMethodCreate(
        name="High School Exam",
        description="Admission based on high school exam results",
        min_score=0.0,
        max_score=30.0
    )
    
    admission_method = create_admission_method_service(db, admission_method_data)
    
    assert admission_method.name == "High School Exam"
    assert admission_method.description == "Admission based on high school exam results"
    assert admission_method.min_score == 0.0
    assert admission_method.max_score == 30.0
    
    # Test tạo admission method với tên đã tồn tại
    with pytest.raises(AlreadyExistsException) as excinfo:
        create_admission_method_service(db, admission_method_data)
    assert "Admission method already exists" in str(excinfo.value)

def test_get_admission_method(db: Session, create_admission_method):
    """Test getting an admission method"""
    # Test lấy admission method theo ID
    admission_method = get_admission_method(db, create_admission_method.id)
    assert admission_method.id == create_admission_method.id
    assert admission_method.name == create_admission_method.name
    
    # Test lấy admission method với ID không tồn tại
    with pytest.raises(NotFoundException) as excinfo:
        get_admission_method(db, 999999)
    assert "Admission method not found" in str(excinfo.value)

def test_get_admission_methods(db: Session, create_admission_method):
    """Test getting all admission methods"""
    # Use the imported service function, not the fixture
    from app.services.university_admission_service import create_admission_method as create_admission_method_service
    
    # Tạo thêm một admission method
    admission_method_data = AdmissionMethodCreate(
        name="School Records",
        description="Admission based on school records",
        min_score=0.0,
        max_score=10.0
    )
    create_admission_method_service(db, admission_method_data)
    
    # Test lấy danh sách admission method
    admission_methods = get_admission_methods(db)
    assert len(admission_methods) >= 2
    method_names = [m.name for m in admission_methods]
    assert "Test Admission Method" in method_names
    assert "School Records" in method_names

def test_create_admission_method_major(db: Session, create_major, create_admission_method):
    """Test creating an admission method major"""
    # Use the imported service function, not the fixture
    from app.services.university_admission_service import create_admission_method_major as create_amm_service
    
    # Test tạo admission method major mới
    admission_method_major_data = AdmissionMethodMajorCreate(
        major_id=create_major.id,
        admission_methods_id=create_admission_method.id
    )
    
    admission_method_major = create_amm_service(db, admission_method_major_data)
    
    assert admission_method_major.major_id == create_major.id
    assert admission_method_major.admission_methods_id == create_admission_method.id
    
    # Test tạo admission method major đã tồn tại
    with pytest.raises(AlreadyExistsException) as excinfo:
        create_amm_service(db, admission_method_major_data)
    assert "Admission method major already exists" in str(excinfo.value)

def test_get_admission_method_major(db: Session, create_admission_method_major):
    """Test getting an admission method major"""
    # Test lấy admission method major theo ID
    admission_method_major = get_admission_method_major(db, create_admission_method_major.id)
    assert admission_method_major.id == create_admission_method_major.id
    assert admission_method_major.major_id == create_admission_method_major.major_id
    assert admission_method_major.admission_methods_id == create_admission_method_major.admission_methods_id
    
    # Test lấy admission method major với ID không tồn tại
    with pytest.raises(NotFoundException) as excinfo:
        get_admission_method_major(db, 999999)
    assert "Admission method major not found" in str(excinfo.value)

def test_get_admission_method_majors(db: Session, create_admission_method_major):
    """Test getting all admission method majors"""
    # Test lấy danh sách admission method major
    admission_method_majors = get_admission_method_majors(db)
    assert len(admission_method_majors) >= 1
    
    # Kiểm tra thông tin
    first_amm = admission_method_majors[0]
    assert first_amm.id == create_admission_method_major.id
    assert first_amm.major_id == create_admission_method_major.major_id
    assert first_amm.admission_methods_id == create_admission_method_major.admission_methods_id

def test_calculate_admission_scores(db: Session, create_subjects, create_subject_group, create_subject_group_details):
    """Test calculating admission scores"""
    subjects = create_subjects
    
    # Test tính điểm xét tuyển với dạng điểm thi THPT
    subject_scores = [
        {
            "subject_id": subjects[0].id,  # Mathematics
            "scores": [8.0]
        },
        {
            "subject_id": subjects[1].id,  # Literature
            "scores": [7.5]
        },
        {
            "subject_id": subjects[2].id,  # Physics
            "scores": [9.0]
        },
        {
            "subject_id": subjects[3].id,  # Chemistry
            "scores": [8.5]  # Không nằm trong group A00
        }
    ]
    
    combinations = calculate_admission_scores(db, "exam", subject_scores)
    
    # Phải có ít nhất 1 kết quả tổ hợp
    assert len(combinations) >= 1
    
    # Kiểm tra kết quả
    group_a00 = next((c for c in combinations if c["group_name"] == "A00"), None)
    assert group_a00 is not None
    # Điểm xét tuyển = (8.0 + 7.5 + 9.0) * 3 / 3 = 24.5 (coefficient = 1.0 cho mỗi môn)
    assert group_a00["score"] == 24.5
    
    # Test với điểm học bạ (semester)
    semester_scores = [
        {
            "subject_id": subjects[0].id,  # Mathematics
            "scores": [8.0, 8.5, 9.0, 7.5, 8.0, 9.5]  # 6 học kỳ
        },
        {
            "subject_id": subjects[1].id,  # Literature
            "scores": [7.0, 7.5, 8.0, 8.5, 7.0, 7.5]
        },
        {
            "subject_id": subjects[2].id,  # Physics
            "scores": [9.0, 8.5, 9.0, 8.5, 9.0, 8.0]
        }
    ]
    
    combinations = calculate_admission_scores(db, "semester", semester_scores)
    
    # Kiểm tra kết quả
    group_a00 = next((c for c in combinations if c["group_name"] == "A00"), None)
    assert group_a00 is not None
    # Điểm trung bình Mathematics = 8.42
    # Điểm trung bình Literature = 7.58
    # Điểm trung bình Physics = 8.67
    # Điểm xét tuyển = (8.42 + 7.58 + 8.67) * 3 / 3 = 24.67
    # Làm tròn 2 chữ số thập phân
    assert abs(group_a00["score"] - 24.67) < 0.1