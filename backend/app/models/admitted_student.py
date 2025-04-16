from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz
from app.models.base import Base

tz = pytz.timezone("Asia/Bangkok")

class AdmittedStudent(Base):
    __tablename__ = "admitted_students"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    student_id = Column(String(10), nullable=False)
    name = Column(String(255))
    gender = Column(Integer, nullable=False)
    identification_id = Column(String(12), nullable=False)
    
    # Khi xóa City thì xóa cả AdmittedStudent liên quan
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)
    major_id = Column(Integer, ForeignKey("majors.id", ondelete="CASCADE"), nullable=False)
    admission_method_id = Column(Integer, ForeignKey("admission_methods.id", ondelete="CASCADE"), nullable=False)
    subject_score_method_group_id = Column(Integer, ForeignKey("subject_score_method_groups.id", ondelete="CASCADE"), nullable=False)
    total_score = Column(Float)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(tz))
    updated_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(tz), onupdate=lambda: datetime.now(tz))
    
    # Relationship với City
    city = relationship("City", back_populates="admitted_students")
    major = relationship("Major", back_populates="admitted_students")
    admission_method = relationship("AdmissionMethod", back_populates="admitted_students")
    subject_score_method_group = relationship("SubjectScoreMethodGroup", back_populates="admitted_students")

