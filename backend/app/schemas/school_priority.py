from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class CityBase(BaseModel):
    city_code: str
    name: str

class CityCreate(CityBase):
    pass

class CityOut(CityBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CityUpdate(BaseModel):
    city_code: Optional[str] = None
    name: Optional[str] = None

class DistrictBase(BaseModel):
    district_code: str
    name: str
    city_id: int

class DistrictCreate(DistrictBase):
    pass

class DistrictOut(DistrictBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class DistrictUpdate(BaseModel):
    district_code: Optional[str] = None
    name: Optional[str] = None
    city_id: Optional[int] = None

class WardBase(BaseModel):
    ward_code: str
    name: str
    district_id: int

class WardCreate(WardBase):
    pass

class WardOut(WardBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class WardUpdate(BaseModel):
    ward_code: Optional[str] = None
    name: Optional[str] = None
    district_id: Optional[int] = None

class SchoolBase(BaseModel):
    school_code: str
    name: str
    address: str
    district_id: int
    priority_area: str  # Khu vực ưu tiên

class SchoolCreate(SchoolBase):
    pass

class SchoolOut(SchoolBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class SchoolUpdate(BaseModel):
    school_code: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    district_id: Optional[int] = None
    priority_area: Optional[str] = None  # Khu vực ưu tiên
