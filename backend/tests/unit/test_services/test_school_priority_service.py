import pytest
from sqlalchemy.orm import Session
from app.services.priority_service import (
    create_city, create_district, create_ward, create_school,
    get_city_by_id, get_district_by_id, get_ward_by_id, get_school_by_id,
    update_city, update_district, update_ward, update_school,
    delete_city, delete_district, delete_ward, delete_school,
    get_search_results, get_districts_by_city, get_wards_by_district, get_schools_by_district
)
from app.models.school_priority import City, District, Ward, School
from app.schemas.school_priority import (
    CityCreate, DistrictCreate, WardCreate, SchoolCreate,
    CityUpdate, DistrictUpdate, WardUpdate, SchoolUpdate
)
from app.core.exceptions import NotFoundException, AlreadyExistsException

@pytest.fixture
def test_city(db: Session):
    """Create a test city"""
    city_data = CityCreate(
        city_code="CTY001",
        name="Test City"
    )
    return create_city(db, city_data)

@pytest.fixture
def test_district(db: Session, test_city):
    """Create a test district"""
    district_data = DistrictCreate(
        district_code="DST001",
        name="Test District",
        city_id=test_city.id
    )
    return create_district(db, district_data)

@pytest.fixture
def test_ward(db: Session, test_district):
    """Create a test ward"""
    ward_data = WardCreate(
        ward_code="WRD001",
        name="Test Ward",
        district_id=test_district.id
    )
    return create_ward(db, ward_data)

@pytest.fixture
def test_school(db: Session, test_district):
    """Create a test school"""
    school_data = SchoolCreate(
        school_code="SCH001",
        name="Test School",
        address="123 Test Street",
        district_id=test_district.id,
        priority_area="KV2"
    )
    return create_school(db, school_data)

def test_create_city(db: Session):
    """Test creating a city"""
    city_data = CityCreate(
        city_code="CIT001",
        name="New City"
    )
    
    city = create_city(db, city_data)
    
    assert city.city_code == city_data.city_code
    assert city.name == city_data.name
    
    # Test creating with existing name
    with pytest.raises(AlreadyExistsException):
        create_city(db, city_data)

def test_get_city_by_id(db: Session, test_city):
    """Test retrieving city by ID"""
    city = get_city_by_id(db, test_city.id)
    
    assert city.id == test_city.id
    assert city.name == test_city.name
    assert city.city_code == test_city.city_code
    
    # Test with non-existent ID
    with pytest.raises(NotFoundException):
        get_city_by_id(db, 99999)

def test_update_city(db: Session, test_city):
    """Test updating a city"""
    update_data = CityUpdate(
        name="Updated City Name",
        city_code="UPC001"
    )
    
    updated_city = update_city(db, test_city.id, update_data)
    
    assert updated_city.name == update_data.name
    assert updated_city.city_code == update_data.city_code
    
    # Test with non-existent ID
    with pytest.raises(NotFoundException):
        update_city(db, 99999, update_data)

def test_delete_city(db: Session):
    """Test deleting a city"""
    # Create city to delete
    city_data = CityCreate(
        city_code="DEL001",
        name="City To Delete"
    )
    city = create_city(db, city_data)
    
    # Test successful deletion
    delete_city(db, city.id)
    
    # Verify city no longer exists
    with pytest.raises(NotFoundException):
        get_city_by_id(db, city.id)
    
    # Test with non-existent ID
    with pytest.raises(NotFoundException):
        delete_city(db, 99999)

def test_create_district(db: Session, test_city):
    """Test creating a district"""
    district_data = DistrictCreate(
        district_code="DIS001",
        name="New District",
        city_id=test_city.id
    )
    
    district = create_district(db, district_data)
    
    assert district.district_code == district_data.district_code
    assert district.name == district_data.name
    assert district.city_id == test_city.id
    
    # Test creating with existing name in same city
    with pytest.raises(AlreadyExistsException):
        create_district(db, district_data)

def test_get_district_by_id(db: Session, test_district):
    """Test retrieving district by ID"""
    district = get_district_by_id(db, test_district.id)
    
    assert district["id"] == test_district.id
    assert district["name"] == test_district.name
    assert district["district_code"] == test_district.district_code
    assert district["city_id"] == test_district.city_id
    assert "city_name" in district
    
    # Test with non-existent ID
    with pytest.raises(NotFoundException):
        get_district_by_id(db, 99999)

def test_update_district(db: Session, test_district):
    """Test updating a district"""
    update_data = DistrictUpdate(
        name="Updated District Name",
        district_code="UPD001"
    )
    
    updated_district = update_district(db, test_district.id, update_data)
    
    assert updated_district.name == update_data.name
    assert updated_district.district_code == update_data.district_code
    
    # Test with non-existent ID
    with pytest.raises(NotFoundException):
        update_district(db, 99999, update_data)

def test_delete_district(db: Session, test_city):
    """Test deleting a district"""
    # Create district to delete
    district_data = DistrictCreate(
        district_code="DEL002",
        name="District To Delete",
        city_id=test_city.id
    )
    district = create_district(db, district_data)
    
    # Test successful deletion
    delete_district(db, district.id)
    
    # Verify district no longer exists
    with pytest.raises(NotFoundException):
        get_district_by_id(db, district.id)
    
    # Test with non-existent ID
    with pytest.raises(NotFoundException):
        delete_district(db, 99999)

def test_create_ward(db: Session, test_district):
    """Test creating a ward"""
    ward_data = WardCreate(
        ward_code="WRD002",
        name="New Ward",
        district_id=test_district.id
    )
    
    ward = create_ward(db, ward_data)
    
    assert ward.ward_code == ward_data.ward_code
    assert ward.name == ward_data.name
    assert ward.district_id == test_district.id
    
    # Test creating with existing name in same district
    with pytest.raises(AlreadyExistsException):
        create_ward(db, ward_data)

def test_get_ward_by_id(db: Session, test_ward):
    """Test retrieving ward by ID"""
    ward = get_ward_by_id(db, test_ward.id)
    
    assert ward.id == test_ward.id
    assert ward.name == test_ward.name
    assert ward.ward_code == test_ward.ward_code
    assert ward.district_id == test_ward.district_id
    
    # Test with non-existent ID
    with pytest.raises(NotFoundException):
        get_ward_by_id(db, 99999)

def test_update_ward(db: Session, test_ward):
    """Test updating a ward"""
    update_data = WardUpdate(
        name="Updated Ward Name",
        ward_code="UPW001"
    )
    
    updated_ward = update_ward(db, test_ward.id, update_data)
    
    assert updated_ward.name == update_data.name
    assert updated_ward.ward_code == update_data.ward_code
    
    # Test with non-existent ID
    with pytest.raises(NotFoundException):
        update_ward(db, 99999, update_data)

def test_delete_ward(db: Session, test_district):
    """Test deleting a ward"""
    # Create ward to delete
    ward_data = WardCreate(
        ward_code="DEL003",
        name="Ward To Delete",
        district_id=test_district.id
    )
    ward = create_ward(db, ward_data)
    
    # Test successful deletion
    delete_ward(db, ward.id)
    
    # Verify ward no longer exists
    with pytest.raises(NotFoundException):
        get_ward_by_id(db, ward.id)
    
    # Test with non-existent ID
    with pytest.raises(NotFoundException):
        delete_ward(db, 99999)

def test_create_school(db: Session, test_district):
    """Test creating a school"""
    school_data = SchoolCreate(
        school_code="SCH002",
        name="New School",
        address="456 School Street",
        district_id=test_district.id,
        priority_area="KV1"
    )
    
    school = create_school(db, school_data)
    
    assert school.school_code == school_data.school_code
    assert school.name == school_data.name
    assert school.address == school_data.address
    assert school.district_id == test_district.id
    assert school.priority_area == school_data.priority_area
    
    # Test creating with existing name in same district
    with pytest.raises(AlreadyExistsException):
        create_school(db, school_data)

def test_get_school_by_id(db: Session, test_school):
    """Test retrieving school by ID"""
    school = get_school_by_id(db, test_school.id)
    
    assert school["id"] == test_school.id
    assert school["name"] == test_school.name
    assert school["school_code"] == test_school.school_code
    assert school["district_id"] == test_school.district_id
    assert school["priority_area"] == test_school.priority_area
    assert "district_name" in school
    assert "city_id" in school
    assert "city_name" in school
    
    # Test with non-existent ID
    with pytest.raises(NotFoundException):
        get_school_by_id(db, 99999)

def test_update_school(db: Session, test_school):
    """Test updating a school"""
    update_data = SchoolUpdate(
        name="Updated School Name",
        school_code="UPS001",
        priority_area="KV2NT"
    )
    
    updated_school = update_school(db, test_school.id, update_data)
    
    assert updated_school.name == update_data.name
    assert updated_school.school_code == update_data.school_code
    assert updated_school.priority_area == update_data.priority_area
    
    # Test with non-existent ID
    with pytest.raises(NotFoundException):
        update_school(db, 99999, update_data)

def test_delete_school(db: Session, test_district):
    """Test deleting a school"""
    # Create school to delete
    school_data = SchoolCreate(
        school_code="DEL004",
        name="School To Delete",
        address="789 Delete Street",
        district_id=test_district.id,
        priority_area="KV3"
    )
    school = create_school(db, school_data)
    
    # Test successful deletion
    delete_school(db, school.id)
    
    # Verify school no longer exists
    with pytest.raises(NotFoundException):
        get_school_by_id(db, school.id)
    
    # Test with non-existent ID
    with pytest.raises(NotFoundException):
        delete_school(db, 99999)

def test_get_districts_by_city(db: Session, test_city, test_district):
    """Test getting districts by city"""
    # Create additional district for testing
    district_data = DistrictCreate(
        district_code="DST002",
        name="Second Test District",
        city_id=test_city.id
    )
    create_district(db, district_data)
    
    districts = get_districts_by_city(db, test_city.id)
    
    assert len(districts) >= 2
    district_names = [d.name for d in districts]
    assert test_district.name in district_names
    assert "Second Test District" in district_names
    
    # Test with non-existent city
    with pytest.raises(NotFoundException):
        get_districts_by_city(db, 99999)

def test_get_wards_by_district(db: Session, test_district, test_ward):
    """Test getting wards by district"""
    # Create additional ward for testing
    ward_data = WardCreate(
        ward_code="WRD002",
        name="Second Test Ward",
        district_id=test_district.id
    )
    create_ward(db, ward_data)
    
    wards = get_wards_by_district(db, test_district.id)
    
    assert len(wards) >= 2
    ward_names = [w.name for w in wards]
    assert test_ward.name in ward_names
    assert "Second Test Ward" in ward_names
    
    # Test with non-existent district
    with pytest.raises(NotFoundException):
        get_wards_by_district(db, 99999)

def test_get_schools_by_district(db: Session, test_district, test_school):
    """Test getting schools by district"""
    # Create additional school for testing
    school_data = SchoolCreate(
        school_code="SCH003",
        name="Second Test School",
        address="987 School Avenue",
        district_id=test_district.id,
        priority_area="KV2NT"
    )
    create_school(db, school_data)
    
    schools = get_schools_by_district(db, test_district.id)
    
    assert len(schools) >= 2
    school_names = [s.name for s in schools]
    assert test_school.name in school_names
    assert "Second Test School" in school_names
    
    # Test with non-existent district
    with pytest.raises(NotFoundException):
        get_schools_by_district(db, 99999)

def test_search_results(db: Session, test_city, test_district, test_ward, test_school):
    """Test search functionality"""
    # Make sure we have some consistent search term in the data
    search_term = "Test"
    
    results = get_search_results(db, search_term)
    
    assert "schools" in results
    assert "districts" in results
    assert "wards" in results
    assert "cities" in results
    
    # Check that each section contains at least one result
    assert len(results["schools"]) > 0
    assert len(results["districts"]) > 0
    assert len(results["wards"]) > 0
    assert len(results["cities"]) > 0
    
    # Test with non-existent search term
    with pytest.raises(NotFoundException):
        get_search_results(db, "NonExistentSearchTerm12345")