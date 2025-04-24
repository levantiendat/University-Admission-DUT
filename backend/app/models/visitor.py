from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, Date
from app.models.base import Base
from datetime import datetime
from zoneinfo import ZoneInfo

def now_utc7():
    return datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))

class VisitorCount(Base):
    __tablename__ = "visitor_count"
    
    id = Column(Integer, primary_key=True, index=True)
    total_visitors = Column(Integer, default=0)
    last_updated = Column(
        TIMESTAMP(timezone=True), 
        default=now_utc7, 
        onupdate=now_utc7
    )

class ActiveSession(Base):
    __tablename__ = "active_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    last_activity = Column(
        TIMESTAMP(timezone=True), 
        default=now_utc7, 
        onupdate=now_utc7
    )

class DailyVisitorCount(Base):
    __tablename__ = "daily_visitor_counts"
    
    date = Column(Date, primary_key=True, index=True)
    count = Column(Integer, default=0)
