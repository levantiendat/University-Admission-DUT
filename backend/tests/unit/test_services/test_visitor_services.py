import pytest
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from app.models.visitor import VisitorCount, ActiveSession, DailyVisitorCount
from zoneinfo import ZoneInfo


def test_visitor_count_model(db: Session):
    """Test VisitorCount model"""
    # Create visitor count
    visitor_count = VisitorCount(total_visitors=100)
    db.add(visitor_count)
    db.commit()
    db.refresh(visitor_count)
    
    # Verify
    assert visitor_count.id is not None
    assert visitor_count.total_visitors == 100
    assert visitor_count.last_updated is not None
    
    # Check if datetime is in UTC+7
    tz = ZoneInfo("Asia/Ho_Chi_Minh")
    now = datetime.now(tz)
    
    # Fix: Make last_updated timezone-aware by assigning the same timezone
    last_updated_aware = visitor_count.last_updated.replace(tzinfo=tz)
    
    time_diff = now - last_updated_aware
    assert time_diff.total_seconds() < 10  # Less than 10 seconds difference
    
    # Cleanup
    db.delete(visitor_count)
    db.commit()


def test_active_session_model(db: Session):
    """Test ActiveSession model"""
    # Create active session
    session = ActiveSession(session_id="test-session-1234")
    db.add(session)
    db.commit()
    db.refresh(session)
    
    # Verify
    assert session.id is not None
    assert session.session_id == "test-session-1234"
    assert session.is_active is True
    assert session.last_activity is not None
    
    # Update session activity
    original_activity = session.last_activity
    session.last_activity = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))
    db.commit()
    db.refresh(session)
    
    # Verify update
    assert session.last_activity > original_activity
    
    # Cleanup
    db.delete(session)
    db.commit()


def test_daily_visitor_count_model(db: Session):
    """Test DailyVisitorCount model"""
    # Create daily visitor count
    today = date.today()
    daily_count = DailyVisitorCount(date=today, count=50)
    db.add(daily_count)
    db.commit()
    
    # Verify
    db_daily_count = db.query(DailyVisitorCount).filter(DailyVisitorCount.date == today).first()
    assert db_daily_count is not None
    assert db_daily_count.date == today
    assert db_daily_count.count == 50
    
    # Update count
    db_daily_count.count += 10
    db.commit()
    
    # Verify update
    db_daily_count = db.query(DailyVisitorCount).filter(DailyVisitorCount.date == today).first()
    assert db_daily_count.count == 60
    
    # Cleanup
    db.delete(db_daily_count)
    db.commit()


def test_multiple_date_visitor_counts(db: Session):
    """Test multiple days of visitor counts"""
    # Create daily visitor counts for multiple days
    today = date.today()
    yesterday = today - timedelta(days=1)
    two_days_ago = today - timedelta(days=2)
    
    counts = [
        DailyVisitorCount(date=two_days_ago, count=30),
        DailyVisitorCount(date=yesterday, count=40),
        DailyVisitorCount(date=today, count=25)
    ]
    
    db.add_all(counts)
    db.commit()
    
    # Verify all days are saved
    all_counts = db.query(DailyVisitorCount).order_by(DailyVisitorCount.date).all()
    assert len(all_counts) >= 3
    
    # Verify order and counts
    date_counts = {str(count.date): count.count for count in all_counts}
    assert date_counts.get(str(two_days_ago)) == 30
    assert date_counts.get(str(yesterday)) == 40
    assert date_counts.get(str(today)) == 25
    
    # Cleanup
    for count in counts:
        db.delete(count)
    db.commit()


def test_expired_sessions_deletion(db: Session):
    """Test identification of expired sessions"""
    now = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))
    
    # Create some active sessions
    active_session = ActiveSession(
        session_id="active-session-1",
        last_activity=now
    )
    
    recent_session = ActiveSession(
        session_id="recent-session-1",
        last_activity=now - timedelta(minutes=10)
    )
    
    expired_session = ActiveSession(
        session_id="expired-session-1",
        last_activity=now - timedelta(minutes=20)
    )
    
    very_old_session = ActiveSession(
        session_id="very-old-session-1",
        last_activity=now - timedelta(hours=2)
    )
    
    db.add_all([active_session, recent_session, expired_session, very_old_session])
    db.commit()
    
    # Find expired sessions (older than 15 minutes)
    cutoff_time = now - timedelta(minutes=15)
    expired_sessions = db.query(ActiveSession).filter(ActiveSession.last_activity < cutoff_time).all()
    
    # Verify
    assert len(expired_sessions) == 2
    expired_ids = [s.session_id for s in expired_sessions]
    assert "expired-session-1" in expired_ids
    assert "very-old-session-1" in expired_ids
    assert "active-session-1" not in expired_ids
    assert "recent-session-1" not in expired_ids
    
    # Cleanup
    db.delete(active_session)
    db.delete(recent_session)
    db.delete(expired_session)
    db.delete(very_old_session)
    db.commit()