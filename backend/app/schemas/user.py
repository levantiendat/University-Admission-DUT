from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Các trường dùng chung
class UserBase(BaseModel):
    name: str
    email: str
    phone_number: Optional[str] = None

# Dữ liệu gửi từ client khi đăng ký
class UserCreate(UserBase):
    password: str

# Dữ liệu đăng nhập
class UserLogin(BaseModel):
    email: str
    password: str

# Schema trả về thông tin user
class UserOut(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        orm_mode = True

# Schema trả về token khi đăng nhập/đăng ký
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class UserUpdate(BaseModel):
    name: str
    phone_number: Optional[str] = None
