from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.models.base import Base

class VisitorCount(Base):
    __tablename__ = "visitor_count"
    
    id = Column(Integer, primary_key=True, index=True)
    total_visitors = Column(Integer, default=0)
    last_updated = Column(DateTime, default=func.now(), onupdate=func.now())

class ActiveSession(Base):
    __tablename__ = "active_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    last_activity = Column(DateTime, default=func.now(), onupdate=func.now())