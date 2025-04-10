from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class QuestionBase(BaseModel):
    title: str
    body_text: str

class QuestionCreate(QuestionBase):
    pass

class QuestionOut(QuestionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class QuestionUpdate(BaseModel):
    title: Optional[str] = None
    body_text: Optional[str] = None

class ResponseBase(BaseModel):
    body_text: str
    question_id: int

class ResponseCreate(ResponseBase):
    pass

class ResponseOut(ResponseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ResponseUpdate(BaseModel):
    body_text: Optional[str] = None
    question_id: Optional[int] = None

class ResponseOutWithQuestion(ResponseOut):
    question: QuestionOut

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True