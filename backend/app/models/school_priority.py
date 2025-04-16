from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz
from app.models.base import Base
from .admitted_student import AdmittedStudent
tz = pytz.timezone("Asia/Bangkok")  # GMT+7

class City(Base):
    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True, index=True)
    city_code = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(tz))
    updated_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(tz), onupdate=lambda: datetime.now(tz))
    
    districts = relationship(
        "District",
        back_populates="city",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    
    # Cascade delete: khi City bị xóa, AdmittedStudent liên quan sẽ bị xóa theo
    admitted_students = relationship(
        "AdmittedStudent",
        back_populates="city",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class District(Base):
    __tablename__ = "districts"
    id = Column(Integer, primary_key=True, index=True)
    district_code = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(tz))
    updated_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(tz), onupdate=lambda: datetime.now(tz))

    city = relationship("City", back_populates="districts")
    wards = relationship(
        "Ward",
        back_populates="district",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    schools = relationship(
        "School",
        back_populates="district",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class Ward(Base):
    __tablename__ = "wards"
    id = Column(Integer, primary_key=True, index=True)
    ward_code = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    district_id = Column(Integer, ForeignKey("districts.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(tz))
    updated_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(tz), onupdate=lambda: datetime.now(tz))

    district = relationship("District", back_populates="wards")


class School(Base):
    __tablename__ = "schools"
    id = Column(Integer, primary_key=True, index=True)
    school_code = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=True)
    district_id = Column(Integer, ForeignKey("districts.id", ondelete="CASCADE"), nullable=False)
    priority_area = Column(String(255), nullable=False)  # Khu vực ưu tiên
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(tz))
    updated_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(tz), onupdate=lambda: datetime.now(tz))

    district = relationship("District", back_populates="schools")