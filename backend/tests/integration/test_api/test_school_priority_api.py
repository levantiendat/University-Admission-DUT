import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.school_priority import City, District, Ward, School
import uuid

def test_create_city(client: TestClient, admin_token_headers, user_token_headers):
    """Test creating a city endpoint"""
    city_data = {
        "city_code": f"CT{uuid.uuid4().hex[:8]}",  # Tạo mã ngẫu nhiên
        "name": f"Test City {uuid.uuid4().hex[:8]}"
    }
    
    # Test successful creation with admin token
    response = client.post(
        "/api/priorities/cities",
        json=city_data,
        headers=admin_token_headers
    )
    assert response.status_code == 200
    created_city = response.json()
    assert created_city["name"] == city_data["name"]
    assert created_city["city_code"] == city_data["city_code"]
    
    # Test creation with user token (should fail - not authorized)
    response = client.post(
        "/api/priorities/cities",
        json=city_data,
        headers=user_token_headers
    )
    assert response.status_code == 403
    
    # Test creation without token (should fail)
    response = client.post("/api/priorities/cities", json=city_data)
    assert response.status_code == 401
    

def test_get_cities(client: TestClient, db: Session):
    """Test getting all cities endpoint"""
    # Create cities for testing
    cities = [
        City(city_code=f"CT{i}", name=f"Test City {i}")
        for i in range(1, 4)
    ]
    for city in cities:
        db.add(city)
    db.commit()
    
    # Test successful retrieval
    response = client.get("/api/priorities/cities")
    assert response.status_code == 200
    cities_list = response.json()
    assert isinstance(cities_list, list)
    assert len(cities_list) >= 3
    
    # Check format of returned cities
    for city in cities_list:
        assert "id" in city
        assert "name" in city
        assert "city_code" in city

def test_update_city(client: TestClient, db: Session, admin_token_headers, user_token_headers):
    """Test updating a city endpoint"""
    # Create a city to update
    city = City(city_code="UPD", name="City to Update")
    db.add(city)
    db.commit()
    db.refresh(city)
    
    update_data = {
        "name": "Updated City Name",
        "city_code": "UPC"
    }
    
    # Test successful update with admin token
    response = client.put(
        f"/api/priorities/cities/{city.id}",
        json=update_data,
        headers=admin_token_headers
    )
    assert response.status_code == 200
    updated_city = response.json()
    assert updated_city["name"] == update_data["name"]
    assert updated_city["city_code"] == update_data["city_code"]
    
    # Test update with user token (should fail - not authorized)
    response = client.put(
        f"/api/priorities/cities/{city.id}",
        json=update_data,
        headers=user_token_headers
    )
    assert response.status_code == 403
    
    # Test update without token (should fail)
    response = client.put(
        f"/api/priorities/cities/{city.id}",
        json=update_data
    )
    assert response.status_code == 401
    

def test_delete_city(client: TestClient, db: Session, admin_token_headers, user_token_headers):
    """Test deleting a city endpoint"""
    # Create a city to delete
    city = City(city_code="DEL", name="City to Delete")
    db.add(city)
    db.commit()
    db.refresh(city)
    
    # Test delete with user token (should fail - not authorized)
    response = client.delete(
        f"/api/priorities/cities/{city.id}",
        headers=user_token_headers
    )
    assert response.status_code == 403
    
    # Test delete without token (should fail)
    response = client.delete(f"/api/priorities/cities/{city.id}")
    assert response.status_code == 401
    
    # Test successful delete with admin token
    response = client.delete(
        f"/api/priorities/cities/{city.id}",
        headers=admin_token_headers
    )
    assert response.status_code == 200
    assert response.json()["detail"] == "City deleted successfully"
    
    # Verify city no longer exists
    response = client.get(f"/api/priorities/cities/{city.id}")
    assert response.status_code == 404
    
    # Test delete with non-existent ID
    response = client.delete(
        "/api/priorities/cities/99999",
        headers=admin_token_headers
    )
    assert response.status_code == 404

def test_create_district(client: TestClient, db: Session, admin_token_headers):
    """Test creating a district endpoint"""
    # Create a city for the district
    city = City(city_code="CIT", name="Parent City")
    db.add(city)
    db.commit()
    db.refresh(city)
    
    district_data = {
        "district_code": "DTR",
        "name": "Test District",
        "city_id": city.id
    }
    
    # Test successful creation with admin token
    response = client.post(
        "/api/priorities/districts",
        json=district_data,
        headers=admin_token_headers
    )
    assert response.status_code == 200
    created_district = response.json()
    assert created_district["name"] == district_data["name"]
    assert created_district["district_code"] == district_data["district_code"]
    assert created_district["city_id"] == city.id
    

def test_get_district(client: TestClient, db: Session):
    """Test getting a district by ID"""
    # Create city and district
    city = City(city_code="CTY", name="City for District")
    db.add(city)
    db.commit()
    db.refresh(city)
    
    district = District(district_code="DST", name="District to Get", city_id=city.id)
    db.add(district)
    db.commit()
    db.refresh(district)
    
    # Test successful retrieval
    response = client.get(f"/api/priorities/districts/{district.id}")
    assert response.status_code == 200
    retrieved_district = response.json()
    assert retrieved_district["id"] == district.id
    assert retrieved_district["name"] == district.name
    assert retrieved_district["city_id"] == city.id
    assert "city_name" in retrieved_district
    
    # Test non-existent ID
    response = client.get("/api/priorities/districts/99999")
    assert response.status_code == 404

def test_get_districts_by_city(client: TestClient, db: Session):
    """Test getting districts by city ID"""
    # Create city with multiple districts
    city = City(city_code="CTY2", name="City with Districts")
    db.add(city)
    db.commit()
    db.refresh(city)
    
    districts = [
        District(district_code=f"DS{i}", name=f"District {i}", city_id=city.id)
        for i in range(1, 4)
    ]
    for district in districts:
        db.add(district)
    db.commit()
    
    # Test successful retrieval
    response = client.get(f"/api/priorities/cities/{city.id}/districts")
    assert response.status_code == 200
    districts_list = response.json()
    assert isinstance(districts_list, list)
    assert len(districts_list) == 3
    
    # Test non-existent city ID
    response = client.get("/api/priorities/cities/99999/districts")
    assert response.status_code == 404

def test_create_ward(client: TestClient, db: Session, admin_token_headers):
    """Test creating a ward endpoint"""
    # Create city and district for the ward
    city = City(city_code="CWD", name="City for Ward")
    db.add(city)
    db.commit()
    db.refresh(city)
    
    district = District(district_code="DWD", name="District for Ward", city_id=city.id)
    db.add(district)
    db.commit()
    db.refresh(district)
    
    ward_data = {
        "ward_code": "WRD",
        "name": "Test Ward",
        "district_id": district.id
    }
    
    # Test successful creation with admin token
    response = client.post(
        "/api/priorities/wards",
        json=ward_data,
        headers=admin_token_headers
    )
    assert response.status_code == 200
    created_ward = response.json()
    assert created_ward["name"] == ward_data["name"]
    assert created_ward["ward_code"] == ward_data["ward_code"]
    assert created_ward["district_id"] == district.id

def test_get_wards_by_district(client: TestClient, db: Session):
    """Test getting wards by district ID"""
    # Create city, district with multiple wards
    city = City(city_code="CWA", name="City for Ward API")
    db.add(city)
    db.commit()
    db.refresh(city)
    
    district = District(district_code="DWA", name="District for Ward API", city_id=city.id)
    db.add(district)
    db.commit()
    db.refresh(district)
    
    wards = [
        Ward(ward_code=f"WA{i}", name=f"Ward {i}", district_id=district.id)
        for i in range(1, 4)
    ]
    for ward in wards:
        db.add(ward)
    db.commit()
    
    # Test successful retrieval
    response = client.get(f"/api/priorities/districts/{district.id}/wards")
    assert response.status_code == 200
    wards_list = response.json()
    assert isinstance(wards_list, list)
    assert len(wards_list) == 3

def test_create_school(client: TestClient, db: Session, admin_token_headers):
    """Test creating a school endpoint"""
    # Create city and district for the school
    city = City(city_code="CSC", name="City for School")
    db.add(city)
    db.commit()
    db.refresh(city)
    
    district = District(district_code="DSC", name="District for School", city_id=city.id)
    db.add(district)
    db.commit()
    db.refresh(district)
    
    school_data = {
        "school_code": "SCH",
        "name": "Test School",
        "address": "123 Test Street",
        "district_id": district.id,
        "priority_area": "KV2"
    }
    
    # Test successful creation with admin token
    response = client.post(
        "/api/priorities/schools",
        json=school_data,
        headers=admin_token_headers
    )
    assert response.status_code == 200
    created_school = response.json()
    assert created_school["name"] == school_data["name"]
    assert created_school["school_code"] == school_data["school_code"]
    assert created_school["district_id"] == district.id
    assert created_school["priority_area"] == school_data["priority_area"]

def test_get_schools_by_district(client: TestClient, db: Session):
    """Test getting schools by district ID"""
    # Create city, district with multiple schools
    city = City(city_code="CSP", name="City for School Pages")
    db.add(city)
    db.commit()
    db.refresh(city)
    
    district = District(district_code="DSP", name="District for School Pages", city_id=city.id)
    db.add(district)
    db.commit()
    db.refresh(district)
    
    schools = [
        School(school_code=f"S{i}", name=f"School {i}", 
               address=f"{i} School Street", district_id=district.id, 
               priority_area="KV2")
        for i in range(1, 4)
    ]
    for school in schools:
        db.add(school)
    db.commit()
    
    # Test successful retrieval
    response = client.get(f"/api/priorities/districts/{district.id}/schools")
    assert response.status_code == 200
    schools_list = response.json()
    assert isinstance(schools_list, list)
    assert len(schools_list) == 3

def test_get_schools_by_city(client: TestClient, db: Session):
    """Test getting schools by city ID"""
    # Create city, district with schools
    city = City(city_code="CCS", name="City for City Schools")
    db.add(city)
    db.commit()
    db.refresh(city)
    
    district = District(district_code="DCS", name="District for City Schools", city_id=city.id)
    db.add(district)
    db.commit()
    db.refresh(district)
    
    schools = [
        School(school_code=f"CS{i}", name=f"City School {i}", 
               address=f"{i} City School Avenue", district_id=district.id, 
               priority_area="KV1")
        for i in range(1, 3)
    ]
    for school in schools:
        db.add(school)
    db.commit()
    
    # Test successful retrieval
    response = client.get(f"/api/priorities/cities/{city.id}/schools")
    assert response.status_code == 200
    schools_list = response.json()
    assert isinstance(schools_list, list)
    assert len(schools_list) == 2