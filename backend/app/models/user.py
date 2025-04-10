from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz
from app.core.security import verify_password
from app.models.base import Base  # Dùng Base chung

tz = pytz.timezone("Asia/Bangkok")  # GMT+7

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    role = Column(String(50), default="user")
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz)
    )
    phone_number = Column(String(20), nullable=True)
    
    # Sử dụng tên thuộc tính dạng số nhiều
    questions = relationship(
        "Question",       # dùng tên lớp dưới dạng chuỗi
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    responses = relationship(
        "Response",       # dùng tên lớp dưới dạng chuỗi
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def check_password(self, plain_password: str) -> bool:
        return verify_password(plain_password, self.hashed_password)

from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz
from app.models.base import Base  # Sử dụng Base chung

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    body_text = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(pytz.timezone("Asia/Bangkok"))
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(pytz.timezone("Asia/Bangkok")),
        onupdate=lambda: datetime.now(pytz.timezone("Asia/Bangkok"))
    )
    
    # Sử dụng tên lớp "User" dưới dạng chuỗi, đảm bảo model User đăng ký attribute "questions"
    user = relationship("User", back_populates="questions")
    # Quan hệ với Response: back_populates khớp với relationship trong Response
    responses = relationship(
        "Response",
        back_populates="question",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

class Response(Base):
    __tablename__ = "responses"
    
    id = Column(Integer, primary_key=True, index=True)
    body_text = Column(String(255), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(pytz.timezone("Asia/Bangkok"))
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(pytz.timezone("Asia/Bangkok")),
        onupdate=lambda: datetime.now(pytz.timezone("Asia/Bangkok"))
    )
    
    # Quan hệ với Question
    question = relationship("Question", back_populates="responses")
    # Quan hệ với User
    user = relationship("User", back_populates="responses")
