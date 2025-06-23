import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.university import Faculty, Major, AdmissionMethod, AdmissionMethodMajor

# Import fixtures
from .test_university_admission_fixtures import (
    create_test_faculty, create_test_major, create_test_admission_method
)

def test_get_faculties(client: TestClient, create_test_faculty):
    """Test getting all faculties endpoint"""
    response = client.get("/api/university-admissions/faculties")
    assert response.status_code == 200
    
    faculties = response.json()
    assert isinstance(faculties, list)
    assert len(faculties) > 0
    
    # Kiểm tra xem test faculty có trong danh sách không
    faculty_ids = [f["id"] for f in faculties]
    assert create_test_faculty.id in faculty_ids

def test_create_faculty(client: TestClient, admin_token_headers: dict, user_token_headers: dict):
    """Test creating a faculty endpoint"""
    faculty_data = {
        "name": "Created Faculty API",
        "description": "Faculty created via API",
        "faculty_code": "CFA"
    }
    
    # Test tạo faculty thành công với quyền admin
    response = client.post(
        "/api/university-admissions/faculties",
        json=faculty_data,
        headers=admin_token_headers
    )
    assert response.status_code == 200
    created_faculty = response.json()
    assert created_faculty["name"] == faculty_data["name"]
    assert created_faculty["faculty_code"] == faculty_data["faculty_code"]
    
    # Test tạo faculty với tên đã tồn tại
    response = client.post(
        "/api/university-admissions/faculties",
        json=faculty_data,
        headers=admin_token_headers
    )
    print(f"Response status: {response.status_code}, body: {response.json()}")
    assert response.status_code == 409
    assert "Faculty already exists" in response.json()["detail"]
    
    # Test tạo faculty không có token
    response = client.post(
        "/api/university-admissions/faculties",
        json=faculty_data
    )
    assert response.status_code == 401
    
    # Test với quyền không phải admin
    response = client.post(
        "/api/university-admissions/faculties",
        json=faculty_data,
        headers=user_token_headers
    )
    assert response.status_code == 403

def test_update_faculty(client: TestClient, create_test_faculty, admin_token_headers: dict, user_token_headers: dict):
    """Test updating a faculty endpoint"""
    faculty_id = create_test_faculty.id
    update_data = {
        "name": "Updated Faculty API",
        "description": "Faculty updated via API",
        "faculty_code": "UFA"
    }
    
    # Test cập nhật faculty thành công với quyền admin
    response = client.put(
        f"/api/university-admissions/faculties/{faculty_id}",
        json=update_data,
        headers=admin_token_headers
    )
    assert response.status_code == 200
    updated_faculty = response.json()
    assert updated_faculty["id"] == faculty_id
    assert updated_faculty["name"] == update_data["name"]
    assert updated_faculty["faculty_code"] == update_data["faculty_code"]
    
    # Test cập nhật faculty không có token
    response = client.put(
        f"/api/university-admissions/faculties/{faculty_id}",
        json=update_data
    )
    assert response.status_code == 401
    
    # Test với quyền không phải admin
    response = client.put(
        f"/api/university-admissions/faculties/{faculty_id}",
        json=update_data,
        headers=user_token_headers
    )
    assert response.status_code == 403
    
    # Test với ID không tồn tại
    response = client.put(
        "/api/university-admissions/faculties/999999",
        json=update_data,
        headers=admin_token_headers
    )
    assert response.status_code == 404
    assert "Faculty not found" in response.json()["detail"]

def test_delete_faculty(client: TestClient, db: Session, admin_token_headers: dict, user_token_headers: dict):
    """Test deleting a faculty endpoint"""
    # Tạo faculty để xóa
    faculty = Faculty(
        name="Faculty To Delete API",
        description="Faculty to be deleted via API",
        faculty_code="FTD"
    )
    db.add(faculty)
    db.commit()
    db.refresh(faculty)
    
    # Test xóa faculty thành công với quyền admin
    response = client.delete(
        f"/api/university-admissions/faculties/{faculty.id}",
        headers=admin_token_headers
    )
    assert response.status_code == 200
    deleted_faculty = response.json()
    assert deleted_faculty["id"] == faculty.id
    
    # Kiểm tra faculty đã bị xóa
    response = client.get(f"/api/university-admissions/faculties/{faculty.id}")
    assert response.status_code == 404
    
    # Test xóa faculty không có token
    # Tạo faculty mới để test
    new_faculty = Faculty(
        name="Another Faculty To Delete",
        description="Another faculty to be deleted",
        faculty_code="AFTD"
    )
    db.add(new_faculty)
    db.commit()
    db.refresh(new_faculty)
    
    response = client.delete(
        f"/api/university-admissions/faculties/{new_faculty.id}"
    )
    assert response.status_code == 401
    
    # Test với quyền không phải admin
    response = client.delete(
        f"/api/university-admissions/faculties/{new_faculty.id}",
        headers=user_token_headers
    )
    assert response.status_code == 403
    
    # Test với ID không tồn tại
    response = client.delete(
        "/api/university-admissions/faculties/999999",
        headers=admin_token_headers
    )
    assert response.status_code == 404
    assert "Faculty not found" in response.json()["detail"]

def test_get_faculty_by_id(client: TestClient, create_test_faculty):
    """Test getting a faculty by ID endpoint"""
    faculty_id = create_test_faculty.id
    
    # Test lấy faculty theo ID
    response = client.get(f"/api/university-admissions/faculties/{faculty_id}")
    assert response.status_code == 200
    faculty = response.json()
    assert faculty["id"] == faculty_id
    assert faculty["name"] == create_test_faculty.name
    
    # Test với ID không tồn tại
    response = client.get("/api/university-admissions/faculties/999999")
    assert response.status_code == 404
    assert "Faculty not found" in response.json()["detail"]

def test_get_majors(client: TestClient, create_test_major):
    """Test getting all majors endpoint"""
    response = client.get("/api/university-admissions/majors")
    assert response.status_code == 200
    
    majors = response.json()
    assert isinstance(majors, list)
    assert len(majors) > 0
    
    # Kiểm tra xem test major có trong danh sách không
    major_ids = [m["id"] for m in majors]
    assert create_test_major.id in major_ids

def test_create_major(client: TestClient, create_test_faculty, admin_token_headers: dict, user_token_headers: dict):
    """Test creating a major endpoint"""
    major_data = {
        "faculty_id": create_test_faculty.id,
        "major_code": "APIT",
        "name": "API Testing Major",
        "seats": 100,
        "description": "Major created via API for testing"
    }
    
    # Test tạo major thành công với quyền admin
    response = client.post(
        "/api/university-admissions/majors",
        json=major_data,
        headers=admin_token_headers
    )
    assert response.status_code == 200
    created_major = response.json()
    assert created_major["name"] == major_data["name"]
    assert created_major["major_code"] == major_data["major_code"]
    assert created_major["faculty_id"] == create_test_faculty.id
    
    # Test tạo major với tên đã tồn tại
    response = client.post(
        "/api/university-admissions/majors",
        json=major_data,
        headers=admin_token_headers
    )
    assert response.status_code == 409
    assert "Major already exists" in response.json()["detail"]
    
    # Test tạo major không có token
    response = client.post(
        "/api/university-admissions/majors",
        json=major_data
    )
    assert response.status_code == 401
    
    # Test với quyền không phải admin
    response = client.post(
        "/api/university-admissions/majors",
        json=major_data,
        headers=user_token_headers
    )
    assert response.status_code == 403

def test_update_major(client: TestClient, create_test_major, admin_token_headers: dict, user_token_headers: dict):
    """Test updating a major endpoint"""
    major_id = create_test_major.id
    update_data = {
        "major_code": "UMAJOR",
        "name": "Updated Major API",
        "seats": 150,
        "description": "Major updated via API for testing"
    }
    
    # Test cập nhật major thành công với quyền admin
    response = client.put(
        f"/api/university-admissions/majors/{major_id}",
        json=update_data,
        headers=admin_token_headers
    )
    assert response.status_code == 200
    updated_major = response.json()
    assert updated_major["id"] == major_id
    assert updated_major["name"] == update_data["name"]
    assert updated_major["major_code"] == update_data["major_code"]
    assert updated_major["seats"] == update_data["seats"]
    
    # Test cập nhật major không có token
    response = client.put(
        f"/api/university-admissions/majors/{major_id}",
        json=update_data
    )
    assert response.status_code == 401
    
    # Test với quyền không phải admin
    response = client.put(
        f"/api/university-admissions/majors/{major_id}",
        json=update_data,
        headers=user_token_headers
    )
    assert response.status_code == 403
    
    # Test với ID không tồn tại
    response = client.put(
        "/api/university-admissions/majors/999999",
        json=update_data,
        headers=admin_token_headers
    )
    assert response.status_code == 404
    assert "Major not found" in response.json()["detail"]

def test_delete_major(client: TestClient, db: Session, create_test_faculty, admin_token_headers: dict, user_token_headers: dict):
    """Test deleting a major endpoint"""
    # Tạo major để xóa
    major = Major(
        faculty_id=create_test_faculty.id,
        major_code="MTDAPI",
        name="Major To Delete API",
        seats=100,
        description="Major to be deleted via API"
    )
    db.add(major)
    db.commit()
    db.refresh(major)
    
    # Test xóa major thành công với quyền admin
    response = client.delete(
        f"/api/university-admissions/majors/{major.id}",
        headers=admin_token_headers
    )
    assert response.status_code == 200
    deleted_major = response.json()
    assert deleted_major["id"] == major.id
    
    # Kiểm tra major đã bị xóa
    response = client.get(f"/api/university-admissions/majors/{major.id}")
    assert response.status_code == 404
    
    # Test xóa major không có token
    # Tạo major mới để test
    new_major = Major(
        faculty_id=create_test_faculty.id,
        major_code="AMTD",
        name="Another Major To Delete",
        seats=100,
        description="Another major to be deleted"
    )
    db.add(new_major)
    db.commit()
    db.refresh(new_major)
    
    response = client.delete(
        f"/api/university-admissions/majors/{new_major.id}"
    )
    assert response.status_code == 401
    
    # Test với quyền không phải admin
    response = client.delete(
        f"/api/university-admissions/majors/{new_major.id}",
        headers=user_token_headers
    )
    assert response.status_code == 403
    
    # Test với ID không tồn tại
    response = client.delete(
        "/api/university-admissions/majors/999999",
        headers=admin_token_headers
    )
    assert response.status_code == 404
    assert "Major not found" in response.json()["detail"]

def test_get_major_by_id(client: TestClient, create_test_major):
    """Test getting a major by ID endpoint"""
    major_id = create_test_major.id
    
    # Test lấy major theo ID
    response = client.get(f"/api/university-admissions/majors/{major_id}")
    assert response.status_code == 200
    major = response.json()
    assert major["id"] == major_id
    assert major["name"] == create_test_major.name
    
    # Test với ID không tồn tại
    response = client.get("/api/university-admissions/majors/999999")
    assert response.status_code == 404
    assert "Major not found" in response.json()["detail"]

def test_get_majors_by_faculty(client: TestClient, create_test_faculty, create_test_major):
    """Test getting majors by faculty ID endpoint"""
    faculty_id = create_test_faculty.id
    
    # Test lấy majors theo faculty ID
    response = client.get(f"/api/university-admissions/majors/faculty/{faculty_id}")
    assert response.status_code == 200
    majors = response.json()
    assert isinstance(majors, list)
    assert len(majors) > 0
    
    # Kiểm tra xem test major có trong danh sách không
    major_ids = [m["id"] for m in majors]
    assert create_test_major.id in major_ids
    
    # Test với faculty ID không tồn tại
    response = client.get("/api/university-admissions/majors/faculty/999999")
    assert response.status_code == 404
    assert "Faculty not found" in response.json()["detail"]

def test_get_admission_methods(client: TestClient, create_test_admission_method):
    """Test getting all admission methods endpoint"""
    response = client.get("/api/university-admissions/admission-methods")
    assert response.status_code == 200
    
    admission_methods = response.json()
    assert isinstance(admission_methods, list)
    assert len(admission_methods) > 0
    
    # Kiểm tra xem test admission method có trong danh sách không
    method_ids = [m["id"] for m in admission_methods]
    assert create_test_admission_method.id in method_ids

def test_create_admission_method(client: TestClient, admin_token_headers: dict, user_token_headers: dict):
    """Test creating an admission method endpoint"""
    admission_method_data = {
        "name": "Created Admission Method API",
        "description": "Admission method created via API for testing",
        "min_score": 0.0,
        "max_score": 30.0
    }
    
    # Test tạo admission method thành công với quyền admin
    response = client.post(
        "/api/university-admissions/admission-methods",
        json=admission_method_data,
        headers=admin_token_headers
    )
    assert response.status_code == 200
    created_method = response.json()
    assert created_method["name"] == admission_method_data["name"]
    assert created_method["min_score"] == admission_method_data["min_score"]
    assert created_method["max_score"] == admission_method_data["max_score"]
    
    # Test tạo admission method với tên đã tồn tại
    response = client.post(
        "/api/university-admissions/admission-methods",
        json=admission_method_data,
        headers=admin_token_headers
    )
    assert response.status_code == 409
    assert "Admission method already exists" in response.json()["detail"]
    
    # Test tạo admission method không có token
    response = client.post(
        "/api/university-admissions/admission-methods",
        json=admission_method_data
    )
    assert response.status_code == 401
    
    # Test với quyền không phải admin
    response = client.post(
        "/api/university-admissions/admission-methods",
        json=admission_method_data,
        headers=user_token_headers
    )
    assert response.status_code == 403

def test_update_admission_method(client: TestClient, create_test_admission_method, admin_token_headers: dict, user_token_headers: dict):
    """Test updating an admission method endpoint"""
    method_id = create_test_admission_method.id
    update_data = {
        "name": "Updated Admission Method API",
        "description": "Admission method updated via API for testing",
        "min_score": 5.0,
        "max_score": 25.0
    }
    
    # Test cập nhật admission method thành công với quyền admin
    response = client.put(
        f"/api/university-admissions/admission-methods/{method_id}",
        json=update_data,
        headers=admin_token_headers
    )
    assert response.status_code == 200
    updated_method = response.json()
    assert updated_method["id"] == method_id
    assert updated_method["name"] == update_data["name"]
    assert updated_method["min_score"] == update_data["min_score"]
    assert updated_method["max_score"] == update_data["max_score"]
    
    # Test cập nhật admission method không có token
    response = client.put(
        f"/api/university-admissions/admission-methods/{method_id}",
        json=update_data
    )
    assert response.status_code == 401
    
    # Test với quyền không phải admin
    response = client.put(
        f"/api/university-admissions/admission-methods/{method_id}",
        json=update_data,
        headers=user_token_headers
    )
    assert response.status_code == 403
    
    # Test với ID không tồn tại
    response = client.put(
        "/api/university-admissions/admission-methods/999999",
        json=update_data,
        headers=admin_token_headers
    )
    assert response.status_code == 404
    assert "Admission method not found" in response.json()["detail"]

def test_delete_admission_method(client: TestClient, db: Session, admin_token_headers: dict, user_token_headers: dict):
    """Test deleting an admission method endpoint"""
    # Tạo admission method để xóa
    method = AdmissionMethod(
        name="Admission Method To Delete API",
        description="Admission method to be deleted via API",
        min_score=0.0,
        max_score=30.0
    )
    db.add(method)
    db.commit()
    db.refresh(method)
    
    # Test xóa admission method thành công với quyền admin
    response = client.delete(
        f"/api/university-admissions/admission-methods/{method.id}",
        headers=admin_token_headers
    )
    assert response.status_code == 200
    deleted_method = response.json()
    assert deleted_method["id"] == method.id
    
    # Kiểm tra admission method đã bị xóa
    response = client.get(f"/api/university-admissions/admission-methods/{method.id}")
    assert response.status_code == 404
    
    # Test xóa admission method không có token
    # Tạo admission method mới để test
    new_method = AdmissionMethod(
        name="Another Admission Method To Delete",
        description="Another admission method to be deleted",
        min_score=0.0,
        max_score=30.0
    )
    db.add(new_method)
    db.commit()
    db.refresh(new_method)
    
    response = client.delete(
        f"/api/university-admissions/admission-methods/{new_method.id}"
    )
    assert response.status_code == 401
    
    # Test với quyền không phải admin
    response = client.delete(
        f"/api/university-admissions/admission-methods/{new_method.id}",
        headers=user_token_headers
    )
    assert response.status_code == 403
    
    # Test với ID không tồn tại
    response = client.delete(
        "/api/university-admissions/admission-methods/999999",
        headers=admin_token_headers
    )
    assert response.status_code == 404
    assert "Admission method not found" in response.json()["detail"]

def test_get_admission_method_by_id(client: TestClient, create_test_admission_method):
    """Test getting an admission method by ID endpoint"""
    method_id = create_test_admission_method.id
    
    # Test lấy admission method theo ID
    response = client.get(f"/api/university-admissions/admission-methods/{method_id}")
    assert response.status_code == 200
    method = response.json()
    assert method["id"] == method_id
    assert method["name"] == create_test_admission_method.name
    
    # Test với ID không tồn tại
    response = client.get("/api/university-admissions/admission-methods/999999")
    assert response.status_code == 404
    assert "Admission method not found" in response.json()["detail"]

def test_create_admission_method_major(client: TestClient, create_test_major, create_test_admission_method, admin_token_headers: dict, user_token_headers: dict):
    """Test creating an admission method major endpoint"""
    admission_method_major_data = {
        "major_id": create_test_major.id,
        "admission_methods_id": create_test_admission_method.id
    }
    
    # Test tạo admission method major thành công với quyền admin
    response = client.post(
        "/api/university-admissions/admission-method-majors",
        json=admission_method_major_data,
        headers=admin_token_headers
    )
    assert response.status_code == 200
    created_amm = response.json()
    assert created_amm["major_id"] == create_test_major.id
    assert created_amm["admission_methods_id"] == create_test_admission_method.id
    
    # Test tạo admission method major đã tồn tại
    response = client.post(
        "/api/university-admissions/admission-method-majors",
        json=admission_method_major_data,
        headers=admin_token_headers
    )
    assert response.status_code == 409
    assert "Admission method major already exists" in response.json()["detail"]
    
    # Test tạo admission method major không có token
    response = client.post(
        "/api/university-admissions/admission-method-majors",
        json=admission_method_major_data
    )
    assert response.status_code == 401
    
    # Test với quyền không phải admin
    response = client.post(
        "/api/university-admissions/admission-method-majors",
        json=admission_method_major_data,
        headers=user_token_headers
    )
    assert response.status_code == 403

def test_get_admission_method_majors(client: TestClient, db: Session, create_test_major, create_test_admission_method):
    """Test getting all admission method majors endpoint"""
    # Tạo admission method major để test
    amm = AdmissionMethodMajor(
        major_id=create_test_major.id,
        admission_methods_id=create_test_admission_method.id
    )
    db.add(amm)
    db.commit()
    db.refresh(amm)
    
    # Test lấy danh sách admission method majors
    response = client.get("/api/university-admissions/admission-method-majors")
    assert response.status_code == 200
    
    admission_method_majors = response.json()
    assert isinstance(admission_method_majors, list)
    assert len(admission_method_majors) > 0
    
    # Kiểm tra xem test admission method major có trong danh sách không
    amm_ids = [m["id"] for m in admission_method_majors]
    assert amm.id in amm_ids

def test_get_admission_method_majors_by_major(client: TestClient, db: Session, create_test_major, create_test_admission_method):
    """Test getting admission method majors by major ID endpoint"""
    # Tạo admission method major để test
    amm = AdmissionMethodMajor(
        major_id=create_test_major.id,
        admission_methods_id=create_test_admission_method.id
    )
    db.add(amm)
    db.commit()
    db.refresh(amm)
    
    # Test lấy admission method majors theo major ID
    response = client.get(f"/api/university-admissions/admission-method-majors/major/{create_test_major.id}")
    assert response.status_code == 200
    
    admission_method_majors = response.json()
    assert isinstance(admission_method_majors, list)
    assert len(admission_method_majors) > 0
    
    # Kiểm tra xem test admission method major có trong danh sách không
    amm_ids = [m["id"] for m in admission_method_majors]
    assert amm.id in amm_ids
    
    # Test với major ID không tồn tại
    response = client.get("/api/university-admissions/admission-method-majors/major/999999")
    assert response.status_code == 404
    assert "Major not found" in response.json()["detail"]

def test_calculate_priority(client: TestClient):
    """Test calculate priority endpoint"""
    # Test tính điểm ưu tiên
    request_data = {
        "score": 25.0,
        "bonus_score": 1.0,
        "priority_area": "KV1",
        "priority_object": "ĐT01"
    }
    
    response = client.post(
        "/api/university-admissions/calculate-priority",
        json=request_data
    )
    assert response.status_code == 200
    result = response.json()
    
    # Kiểm tra kết quả tính toán
    assert result["origin_point"] == 25.0
    assert result["bonus_score"] == 1.0
    assert result["origin_priority"] == 2.75  # KV1 (0.75) + ĐT01 (2.0)
    assert result["total_point"] > 25.0  # Tổng điểm phải lớn hơn điểm gốc
    
    # Test với điểm thấp (không cần giảm điểm ưu tiên)
    low_score_data = {
        "score": 20.0,
        "priority_area": "KV1",
        "priority_object": "ĐT01"
    }
    
    response = client.post(
        "/api/university-admissions/calculate-priority",
        json=low_score_data
    )
    assert response.status_code == 200
    result = response.json()
    
    # Điểm ưu tiên khi điểm gốc <= 22.5 thì không bị giảm
    assert result["origin_priority"] == result["convert_priority"]
    
    # Test với điểm cao (cần giảm điểm ưu tiên)
    high_score_data = {
        "score": 28.0,
        "priority_area": "KV1",
        "priority_object": "ĐT01"
    }
    
    response = client.post(
        "/api/university-admissions/calculate-priority",
        json=high_score_data
    )
    assert response.status_code == 200
    result = response.json()
    
    # Điểm ưu tiên khi điểm gốc > 22.5 thì bị giảm
    assert result["convert_priority"] < result["origin_priority"]