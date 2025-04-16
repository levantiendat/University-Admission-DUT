from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class AdmittedStudentBase(BaseModel):
    year: int
    student_id: str
    name: str
    gender: int
    identification_id: str
    city_id: int
    major_id: int
    admission_method_id: int
    subject_score_method_group_id: int
    total_score: float

class AdmittedStudentCreate(AdmittedStudentBase):
    pass

class AdmittedStudentOut(AdmittedStudentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class AdmittedStudentUpdate(BaseModel):
    year: Optional[int] = None
    student_id: str
    name: str
    gender: Optional[int] = None
    identification_id: str
    city_id: Optional[int] = None
    major_id: Optional[int] = None
    admission_method_id: Optional[int] = None
    subject_score_method_group_id: Optional[int] = None
    total_score: Optional[float] = None

