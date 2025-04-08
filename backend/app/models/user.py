from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pytz
from app.core.security import verify_password

Base = declarative_base()
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

    def check_password(self, plain_password: str) -> bool:
        return verify_password(plain_password, self.hashed_password)
