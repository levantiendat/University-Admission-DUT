from app.models.school_priority import City, District, Ward, School
from sqlalchemy.orm import Session
from app.schemas.school_priority import CityCreate, DistrictCreate, WardCreate, SchoolCreate
from app.schemas.school_priority import CityUpdate, DistrictUpdate, WardUpdate, SchoolUpdate

from app.core.exceptions import NotFoundException, AlreadyExistsException
from app.core.exceptions import ForbiddenException

def create_city(db: Session, city_in: CityCreate) -> City:
    existing_city = db.query(City).filter(City.name == city_in.name).first()
    if existing_city:
        raise AlreadyExistsException(detail="City already exists")
    new_city = City(name=city_in.name, city_code=city_in.city_code)
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city

def create_district(db: Session, district_in: DistrictCreate) -> District:
    new_district = District(name=district_in.name, city_id=district_in.city_id, district_code=district_in.district_code)
    existing_district = db.query(District).filter(District.name == district_in.name, District.city_id == district_in.city_id).first()
    if existing_district:
        raise AlreadyExistsException(detail="District already exists")
    db.add(new_district)
    db.commit()
    db.refresh(new_district)
    return new_district

def create_ward(db: Session, ward_in: WardCreate) -> Ward:
    new_ward = Ward(name=ward_in.name, district_id=ward_in.district_id, ward_code=ward_in.ward_code)
    existing_ward = db.query(Ward).filter(Ward.name == ward_in.name, Ward.district_id == ward_in.district_id).first()
    if existing_ward:
        raise AlreadyExistsException(detail="Ward already exists")
    db.add(new_ward)
    db.commit()
    db.refresh(new_ward)
    return new_ward

def create_school(db: Session, school_in: SchoolCreate) -> School:
    new_school = School(name=school_in.name, district_id=school_in.district_id, school_code=school_in.school_code, priority_area=school_in.priority_area, address=school_in.address)
    existing_school = db.query(School).filter(School.name == school_in.name, School.district_id == school_in.district_id).first()
    if existing_school:
        raise AlreadyExistsException(detail="School already exists")
    db.add(new_school)
    db.commit()
    db.refresh(new_school)
    return new_school

def update_city(db: Session, city_id: int, city_in: CityUpdate) -> City:
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise NotFoundException(detail="City not found")
    if city_in.name and db.query(City).filter(City.name == city_in.name).first():
        raise AlreadyExistsException(detail="City already exists")
    for key, value in city_in.dict(exclude_unset=True).items():
        setattr(city, key, value)
    db.commit()
    db.refresh(city)
    return city

def update_district(db: Session, district_id: int, district_in: DistrictUpdate) -> District:
    district = db.query(District).filter(District.id == district_id).first()
    if not district:
        raise NotFoundException(detail="District not found")
    if district_in.name and db.query(District).filter(District.name == district_in.name).first():
        raise AlreadyExistsException(detail="District already exists")
    for key, value in district_in.dict(exclude_unset=True).items():
        setattr(district, key, value)
    db.commit()
    db.refresh(district)
    return district

def update_ward(db: Session, ward_id: int, ward_in: WardUpdate) -> Ward:
    ward = db.query(Ward).filter(Ward.id == ward_id).first()
    if not ward:
        raise NotFoundException(detail="Ward not found")
    if ward_in.name and db.query(Ward).filter(Ward.name == ward_in.name).first():
        raise AlreadyExistsException(detail="Ward already exists")
    for key, value in ward_in.dict(exclude_unset=True).items():
        setattr(ward, key, value)
    db.commit()
    db.refresh(ward)
    return ward

def update_school(db: Session, school_id: int, school_in: SchoolUpdate) -> School:
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise NotFoundException(detail="School not found")
    if school_in.name and db.query(School).filter(School.name == school_in.name).first():
        raise AlreadyExistsException(detail="School already exists")
    for key, value in school_in.dict(exclude_unset=True).items():
        setattr(school, key, value)
    db.commit()
    db.refresh(school)
    return school

def delete_city(db: Session, city_id: int) -> None:
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise NotFoundException(detail="City not found")

    # Lấy toàn bộ district thuộc city
    districts = db.query(District).filter(District.city_id == city_id).all()
    for district in districts:
        # Xoá các school trong mỗi district
        db.query(School).filter(School.district_id == district.id).delete()
        # Xoá các ward trong mỗi district
        db.query(Ward).filter(Ward.district_id == district.id).delete()

    # Xoá các district sau khi xoá ward và school
    db.query(District).filter(District.city_id == city_id).delete()
    db.delete(city)
    db.commit()

def delete_district(db: Session, district_id: int) -> None:
    district = db.query(District).filter(District.id == district_id).first()
    if not district:
        raise NotFoundException(detail="District not found")

    # Xoá các school và ward liên quan
    db.query(School).filter(School.district_id == district_id).delete()
    db.query(Ward).filter(Ward.district_id == district_id).delete()

    db.delete(district)
    db.commit()

def delete_ward(db: Session, ward_id: int) -> None:
    ward = db.query(Ward).filter(Ward.id == ward_id).first()
    if not ward:
        raise NotFoundException(detail="Ward not found")
    db.delete(ward)
    db.commit()

def delete_school(db: Session, school_id: int) -> None:
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise NotFoundException(detail="School not found")
    db.delete(school)
    db.commit()

def get_city_by_id(db: Session, city_id: int) -> City:
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise NotFoundException(detail="City not found")
    return city

def get_district_by_id(db: Session, district_id: int) -> District:
    district = db.query(District).filter(District.id == district_id).first()
    if not district:
        raise NotFoundException(detail="District not found")
    return district

def get_ward_by_id(db: Session, ward_id: int) -> Ward:
    ward = db.query(Ward).filter(Ward.id == ward_id).first()
    if not ward:
        raise NotFoundException(detail="Ward not found")
    return ward

def get_school_by_id(db: Session, school_id: int) -> School:
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise NotFoundException(detail="School not found")
    return school

def get_districts_by_city(db: Session, city_id: int) -> list[District]:
    districts = db.query(District).filter(District.city_id == city_id).all()
    if not districts:
        raise NotFoundException(detail="No districts found for this city")
    return districts

def get_wards_by_district(db: Session, district_id: int) -> list[Ward]:
    wards = db.query(Ward).filter(Ward.district_id == district_id).all()
    if not wards:
        raise NotFoundException(detail="No wards found for this district")
    return wards

def get_schools_by_district(db: Session, district_id: int) -> list[School]:
    schools = db.query(School).filter(School.district_id == district_id).all()
    if not schools:
        raise NotFoundException(detail="No schools found for this district")
    return schools

def get_cities(db: Session) -> list[City]:
    cities = db.query(City).all()
    if not cities:
        raise NotFoundException(detail="No cities found")
    return cities
def get_districts(db: Session) -> list[District]:
    districts = db.query(District).all()
    if not districts:
        raise NotFoundException(detail="No districts found")
    return districts
def get_wards(db: Session) -> list[Ward]:
    wards = db.query(Ward).all()
    if not wards:
        raise NotFoundException(detail="No wards found")
    return wards
def get_schools(db: Session) -> list[School]:
    schools = db.query(School).all()
    if not schools:
        raise NotFoundException(detail="No schools found")
    return schools

def get_city_by_code(db: Session, city_code: str) -> City:
    city = db.query(City).filter(City.city_code == city_code).first()
    if not city:
        raise NotFoundException(detail="City not found")
    return city
def get_district_by_code(db: Session, district_code: str) -> District:
    district = db.query(District).filter(District.district_code == district_code).first()
    if not district:
        raise NotFoundException(detail="District not found")
    return district
def get_ward_by_code(db: Session, ward_code: str) -> Ward:
    ward = db.query(Ward).filter(Ward.ward_code == ward_code).first()
    if not ward:
        raise NotFoundException(detail="Ward not found")
    return ward
def get_school_by_code(db: Session, school_code: str) -> School:
    school = db.query(School).filter(School.school_code == school_code).first()
    if not school:
        raise NotFoundException(detail="School not found")
    return school
def get_city_by_name(db: Session, city_name: str) -> City:
    city = db.query(City).filter(City.name == city_name).first()
    if not city:
        raise NotFoundException(detail="City not found")
    return city
def get_district_by_name(db: Session, district_name: str) -> District:
    district = db.query(District).filter(District.name == district_name).first()
    if not district:
        raise NotFoundException(detail="District not found")
    return district
def get_ward_by_name(db: Session, ward_name: str) -> Ward:
    ward = db.query(Ward).filter(Ward.name == ward_name).first()
    if not ward:
        raise NotFoundException(detail="Ward not found")
    return ward
def get_school_by_name(db: Session, school_name: str) -> School:
    school = db.query(School).filter(School.name == school_name).first()
    if not school:
        raise NotFoundException(detail="School not found")
    return school

def get_search_results(db: Session, search: str) -> dict:
    results_school = db.query(School).filter(School.name.ilike(f"%{search}%")).all()
    results_district = db.query(District).filter(District.name.ilike(f"%{search}%")).all()
    results_ward = db.query(Ward).filter(Ward.name.ilike(f"%{search}%")).all()
    results_city = db.query(City).filter(City.name.ilike(f"%{search}%")).all()

    if not any([results_school, results_district, results_ward, results_city]):
        raise NotFoundException(detail="No results found")

    return {
        "schools": [{"id": s.id, "name": s.name} for s in results_school],
        "districts": [{"id": d.id, "name": d.name} for d in results_district],
        "wards": [{"id": w.id, "name": w.name} for w in results_ward],
        "cities": [{"id": c.id, "name": c.name} for c in results_city],
    }
