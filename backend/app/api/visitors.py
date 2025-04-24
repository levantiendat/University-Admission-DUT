from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.visitor import VisitorCount, ActiveSession, DailyVisitorCount
from datetime import datetime, timedelta
from uuid import uuid4
import json
from typing import Dict
from pydantic import BaseModel
from zoneinfo import ZoneInfo
from datetime import date
from fastapi import Query
from typing import List, Optional

def get_today_utc7():
    return datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).date()

def now_utc7() -> datetime:
    return datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))

router = APIRouter()

class VisitorStats(BaseModel):
    current_visitors: int
    total_visitors: int

class DailyStat(BaseModel):
    date: date
    count: int

def cleanup_sessions(db: Session):
    cutoff_time = now_utc7() - timedelta(minutes=15)
    expired_sessions = db.query(ActiveSession).filter(ActiveSession.last_activity < cutoff_time).all()
    
    for session in expired_sessions:
        db.delete(session)
    
    db.commit()
    return len(expired_sessions)

@router.get("/stats", response_model=VisitorStats)
def get_visitor_stats(request: Request, db: Session = Depends(get_db)):
    cleanup_sessions(db)

    session_id = request.session.get("visitor_session_id")
    is_new_visitor = False

    if not session_id:
        session_id = str(uuid4())
        request.session["visitor_session_id"] = session_id
        is_new_visitor = True
    else:
        db_session = db.query(ActiveSession).filter(ActiveSession.session_id == session_id).first()
        if db_session:
            db_session.last_activity = now_utc7()
            db.commit()
        else:
            is_new_visitor = True

    if is_new_visitor:
        # Tạo session mới
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

    # Tăng lượt truy cập theo ngày (dù là new hay không)
    today = now_utc7().date()
    daily_count = db.query(DailyVisitorCount).filter(DailyVisitorCount.date == today).first()
    if not daily_count:
        daily_count = DailyVisitorCount(date=today, count=1)
        db.add(daily_count)
    else:
        daily_count.count += 1

    db.commit()

    # Đếm số người đang truy cập
    current_visitors = db.query(ActiveSession).filter(ActiveSession.is_active == True).count()
    visitor_count = db.query(VisitorCount).first()
    total_visitors = visitor_count.total_visitors if visitor_count else 0

    return VisitorStats(current_visitors=current_visitors, total_visitors=total_visitors)


@router.post("/heartbeat")
def heartbeat(request: Request, db: Session = Depends(get_db)):
    session_id = request.session.get("visitor_session_id")
    if session_id:
        db_session = db.query(ActiveSession).filter(ActiveSession.session_id == session_id).first()
        if db_session:
            db_session.last_activity = now_utc7()
            db.commit()
            return {"status": "updated"}
    return {"status": "session not found"}


@router.get("/stats/daily", response_model=List[DailyStat])
def get_daily_stats(
    start: Optional[date] = Query(None),
    end: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    if not start:
        start = get_today_utc7()
    if not end:
        end = get_today_utc7()
    
    results = (
        db.query(DailyVisitorCount)
        .filter(DailyVisitorCount.date >= start)
        .filter(DailyVisitorCount.date <= end)
        .order_by(DailyVisitorCount.date)
        .all()
    )
    return results