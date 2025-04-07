from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
import datetime
from app.core.security import verify_password

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    role = Column(String(50), default="user")  # Các giá trị: admin, user, instructor
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    phone_number = Column(String(20), nullable=True)

    def check_password(self, plain_password: str) -> bool:
        return verify_password(plain_password, self.hashed_password)
