from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.visitor import VisitorCount, ActiveSession
from datetime import datetime, timedelta
from uuid import uuid4
import json
from typing import Dict
from pydantic import BaseModel

router = APIRouter()

class VisitorStats(BaseModel):
    current_visitors: int
    total_visitors: int

# Xóa session hết hạn (không hoạt động trong 15 phút)
def cleanup_sessions(db: Session):
    cutoff_time = datetime.utcnow() - timedelta(minutes=15)
    expired_sessions = db.query(ActiveSession).filter(ActiveSession.last_activity < cutoff_time).all()
    
    for session in expired_sessions:
        db.delete(session)
    
    db.commit()
    return len(expired_sessions)

@router.get("/stats", response_model=VisitorStats)
def get_visitor_stats(request: Request, db: Session = Depends(get_db)):
    # Xóa các session hết hạn
    cleanup_sessions(db)
    
    # Kiểm tra session ID
    session_id = request.session.get("visitor_session_id")
    
    if not session_id:
        # Nếu chưa có, tạo ID mới và tăng tổng số người truy cập
        session_id = str(uuid4())
        request.session["visitor_session_id"] = session_id
        
        # Thêm session mới
        db_session = ActiveSession(session_id=session_id)
        db.add(db_session)
        
        # Tăng tổng số người truy cập
        visitor_count = db.query(VisitorCount).first()
        if not visitor_count:
            visitor_count = VisitorCount(total_visitors=1)
            db.add(visitor_count)
        else:
            visitor_count.total_visitors += 1
        
        db.commit()
    else:
        # Nếu đã có, cập nhật thời gian hoạt động cuối
        db_session = db.query(ActiveSession).filter(ActiveSession.session_id == session_id).first()
        if db_session:
            db_session.last_activity = datetime.utcnow()
            db.commit()
        else:
            # Nếu không tìm thấy (có thể đã bị xóa do hết hạn), tạo mới
            db_session = ActiveSession(session_id=session_id)
            db.add(db_session)
            
            # Tăng tổng số người truy cập
            visitor_count = db.query(VisitorCount).first()
            if not visitor_count:
                visitor_count = VisitorCount(total_visitors=1)
                db.add(visitor_count)
            else:
                visitor_count.total_visitors += 1
            
            db.commit()
    
    # Đếm số người đang truy cập
    current_visitors = db.query(ActiveSession).filter(ActiveSession.is_active == True).count()
    
    # Lấy tổng số người truy cập
    visitor_count = db.query(VisitorCount).first()
    total_visitors = visitor_count.total_visitors if visitor_count else 0
    
    return VisitorStats(current_visitors=current_visitors, total_visitors=total_visitors)

@router.post("/heartbeat")
def heartbeat(request: Request, db: Session = Depends(get_db)):
    session_id = request.session.get("visitor_session_id")
    if session_id:
        db_session = db.query(ActiveSession).filter(ActiveSession.session_id == session_id).first()
        if db_session:
            db_session.last_activity = datetime.utcnow()
            db.commit()
            return {"status": "updated"}
    
    return {"status": "session not found"}