from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.schemas.school_priority import CityCreate, DistrictCreate, WardCreate, SchoolCreate
from app.schemas.school_priority import CityUpdate, DistrictUpdate, WardUpdate, SchoolUpdate
from app.schemas.school_priority import CityOut, DistrictOut, WardOut, SchoolOut, SchoolOut_Full
from app.core.exceptions import NotFoundException, AlreadyExistsException, ForbiddenException
from app.models.school_priority import City, District, Ward, School
from app.services.priority_service import create_city, create_district, create_ward, create_school
from app.services.priority_service import update_city, update_district, update_ward, update_school
from app.services.priority_service import get_city_by_id, get_district_by_id, get_ward_by_id, get_school_by_id
from app.services.priority_service import get_cities, get_districts, get_wards, get_schools
from app.services.priority_service import get_city_by_code, get_district_by_code, get_ward_by_code, get_school_by_code
from app.services.priority_service import get_city_by_name, get_district_by_name, get_ward_by_name, get_school_by_name, get_search_results
from app.services.priority_service import delete_city, delete_district, delete_ward, delete_school
from app.services.priority_service import get_districts_by_city, get_wards_by_district, get_schools_by_district, get_school_by_city
from app.db.session import get_db
from app.core.security import verify_access_token, create_access_token
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
router = APIRouter()

@router.post("/cities", response_model=CityOut)
def create_city_endpoint(
    city: CityCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception

    if user.role != "admin":
        raise ForbiddenException(detail="You do not have permission to perform this action")

    return create_city(db=db, city_in=city)

@router.get("/cities", response_model=list[CityOut])
def get_cities_endpoint(
    db: Session = Depends(get_db)
):
    return get_cities(db=db)

@router.get("/cities/{city_id}", response_model=CityOut)
def get_city_endpoint(
    city_id: int,
    db: Session = Depends(get_db)
):
    city = get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise NotFoundException(detail=f"City with id code {city_id} not found")
    return city

@router.put("/cities/{city_id}", response_model=CityOut)
def update_city_endpoint(
    city_id: int,
    city_update: CityUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception

    if user.role != "admin":
        raise ForbiddenException(detail="You do not have permission to perform this action")

    city = get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise NotFoundException(detail=f"City with code {city_id} not found")

    return update_city(db=db, city_id=city_id, city_in=city_update)

@router.delete("/cities/{city_id}")
def delete_city_endpoint(
    city_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception

    if user.role != "admin":
        raise ForbiddenException(detail="You do not have permission to perform this action")

    delete_city(db=db, city_id=city_id)

    return {"detail": "City deleted successfully"}

@router.post("/districts", response_model=DistrictOut)
def create_district_endpoint(
    district: DistrictCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception

    if user.role != "admin":
        raise ForbiddenException(detail="You do not have permission to perform this action")

    return create_district(db=db, district_in=district)

@router.get("/districts", response_model=list[DistrictOut])
def get_districts_endpoint(
    db: Session = Depends(get_db)
):
    return get_districts(db=db)

@router.get("/districts/{district_id}", response_model=dict)
def get_district_endpoint(
    district_id: int,
    db: Session = Depends(get_db)
):
    district = get_district_by_id(db=db, district_id=district_id)
    if not district:
        raise NotFoundException(detail=f"District with id code {district_id} not found")
    return district

@router.put("/districts/{district_id}", response_model=DistrictOut)
def update_district_endpoint(
    district_id: int,
    district_update: DistrictUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception

    if user.role != "admin":
        raise ForbiddenException(detail="You do not have permission to perform this action")

    district = get_district_by_id(db=db, district_id=district_id)
    if not district:
        raise NotFoundException(detail=f"District with code {district_id} not found")

    return update_district(db=db, district_id=district_id, district_in=district_update)

@router.delete("/districts/{district_id}")
def delete_district_endpoint(
    district_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception

    if user.role != "admin":
        raise ForbiddenException(detail="You do not have permission to perform this action")

    delete_district(db=db, district_id=district_id)

    return {"detail": "District deleted successfully"}

@router.post("/wards", response_model=WardOut)
def create_ward_endpoint(
    ward: WardCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception

    if user.role != "admin":
        raise ForbiddenException(detail="You do not have permission to perform this action")

    return create_ward(db=db, ward_in=ward)

@router.get("/wards", response_model=list[WardOut])
def get_wards_endpoint(
    db: Session = Depends(get_db)
):
    return get_wards(db=db)

@router.get("/wards/{ward_id}", response_model=WardOut)
def get_ward_endpoint(
    ward_id: int,
    db: Session = Depends(get_db)
):
    ward = get_ward_by_id(db=db, ward_id=ward_id)
    if not ward:
        raise NotFoundException(detail=f"Ward with id code {ward_id} not found")
    return ward

@router.put("/wards/{ward_id}", response_model=WardOut)
def update_ward_endpoint(
    ward_id: int,
    ward_update: WardUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception

    if user.role != "admin":
        raise ForbiddenException(detail="You do not have permission to perform this action")

    ward = get_ward_by_id(db=db, ward_id=ward_id)
    if not ward:
        raise NotFoundException(detail=f"Ward with code {ward_id} not found")

    return update_ward(db=db, ward_id=ward_id, ward_in=ward_update)

@router.delete("/wards/{ward_id}")
def delete_ward_endpoint(
    ward_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception

    if user.role != "admin":
        raise ForbiddenException(detail="You do not have permission to perform this action")

    delete_ward(db=db, ward_id=ward_id)

    return {"detail": "Ward deleted successfully"}

@router.post("/schools", response_model=SchoolOut)
def create_school_endpoint(
    school: SchoolCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception

    if user.role != "admin":
        raise ForbiddenException(detail="You do not have permission to perform this action")

    return create_school(db=db, school_in=school)

@router.get("/schools", response_model=list[SchoolOut])
def get_schools_endpoint(
    page: int = 1,  # Số trang, mặc định là 1
    db: Session = Depends(get_db)
):
    """
    API để lấy danh sách trường học với phân trang.
    Mỗi trang chứa tối đa 200 phần tử.
    """
    page_size = 200  # Số lượng phần tử mỗi trang
    offset = (page - 1) * page_size  # Tính vị trí bắt đầu

    schools = db.query(School).offset(offset).limit(page_size).all()
    return schools

@router.get("/schools/{school_id}", response_model=dict)
def get_school_endpoint(
    school_id: int,
    db: Session = Depends(get_db)
):
    school = get_school_by_id(db=db, school_id=school_id)
    if not school:
        raise NotFoundException(detail=f"School with id code {school_id} not found")
    return school

@router.put("/schools/{school_id}", response_model=SchoolOut)
def update_school_endpoint(
    school_id: int,
    school_update: SchoolUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception

    if user.role != "admin":
        raise ForbiddenException(detail="You do not have permission to perform this action")

    school = get_school_by_id(db=db, school_id=school_id)
    if not school:
        raise NotFoundException(detail=f"School with code {school_id} not found")

    return update_school(db=db, school_id=school_id, school_in=school_update)

@router.delete("/schools/{school_id}")
def delete_school_endpoint(
    school_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception

    if user.role != "admin":
        raise ForbiddenException(detail="You do not have permission to perform this action")

    delete_school(db=db, school_id=school_id)

    return {"detail": "School deleted successfully"}

@router.get("/search", response_model=dict)
def search_endpoint(
    q: str,
    db: Session = Depends(get_db)
):
    return get_search_results(db=db, search=q)

@router.get("/cities/{city_id}/districts", response_model=list[DistrictOut])
def get_districts_by_city_endpoint(
    city_id: int,
    db: Session = Depends(get_db)
):
    """
    API để lấy danh sách quận/huyện theo city_id.
    """
    return get_districts_by_city(db=db, city_id=city_id)


@router.get("/districts/{district_id}/wards", response_model=list[WardOut])
def get_wards_by_district_endpoint(
    district_id: int,
    db: Session = Depends(get_db)
):
    """
    API để lấy danh sách phường/xã theo district_id.
    """
    return get_wards_by_district(db=db, district_id=district_id)


@router.get("/districts/{district_id}/schools", response_model=list[SchoolOut])
def get_schools_by_district_endpoint(
    district_id: int,
    db: Session = Depends(get_db)
):
    """
    API để lấy danh sách trường học theo district_id.
    """
    return get_schools_by_district(db=db, district_id=district_id)

@router.get("/cities/{city_id}/schools", response_model=list[SchoolOut])
def get_schools_by_city_endpoint(
    city_id: int,
    db: Session = Depends(get_db)
):
    """
    API để lấy danh sách trường học theo city_id.
    """
    return get_school_by_city(db=db, city_id=city_id)