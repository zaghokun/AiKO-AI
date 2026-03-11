"""
Chat session manager - handles 24h session lifecycle
"""

from datetime import datetime, timedelta, date, timezone
from sqlalchemy.orm import Session
from sqlalchemy import and_
from .models import User, ChatSession, Message
from ..config import settings
import uuid

class SessionManager:
    """Manages chat sessions with 24h auto-reset"""
    
    @staticmethod
    def get_or_create_user(db: Session, username: str = "default_user") -> User:
        """Get existing user or create new one"""
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            user = User(username=username)
            db.add(user)
            db.commit()
            db.refresh(user)
        
        return user
    
    @staticmethod
    def get_active_session(db: Session, user_id: uuid.UUID) -> ChatSession | None:
        """
        Get active session for user
        Returns None if no active session or session expired
        """
        now = datetime.now(timezone.utc)
        today = date.today()
        
        # Find active session for today
        session = db.query(ChatSession).filter(
            and_(
                ChatSession.user_id == user_id,
                ChatSession.session_date == today,
                ChatSession.is_active == True,
                ChatSession.expires_at > now
            )
        ).first()
        
        # If session exists but expired, deactivate it
        if session and session.expires_at <= now:
            session.is_active = False
            db.commit()
            return None
        
        return session
    
    @staticmethod
    def create_new_session(db: Session, user_id: uuid.UUID) -> ChatSession:
        """
        Create new chat session
        Expires after SESSION_DURATION_HOURS (default: 24h)
        """
        now = datetime.now(timezone.utc)
        today = date.today()
        
        # Deactivate any old sessions for this user on this date
        db.query(ChatSession).filter(
            and_(
                ChatSession.user_id == user_id,
                ChatSession.session_date == today
            )
        ).update({"is_active": False})
        
        # Create new session
        session = ChatSession(
            user_id=user_id,
            session_date=today,
            started_at=now,
            expires_at=now + timedelta(hours=settings.session_duration_hours),
            message_count=0,
            is_active=True
        )
        
        db.add(session)
        db.commit()
        db.refresh(session)
        
        return session
    
    @staticmethod
    def get_or_create_session(db: Session, username: str = "default_user") -> ChatSession:
        """
        Get active session or create new one
        Main entry point for session management
        """
        # Get or create user
        user = SessionManager.get_or_create_user(db, username)
        
        # Get active session
        session = SessionManager.get_active_session(db, user.id)
        
        # Create new session if needed
        if not session:
            session = SessionManager.create_new_session(db, user.id)
        
        return session
    
    @staticmethod
    def add_message(
        db: Session,
        session_id: uuid.UUID,
        role: str,
        content: str,
        tokens_used: int | None = None
    ) -> Message:
        """Add message to session"""
        message = Message(
            session_id=session_id,
            role=role,
            content=content,
            tokens_used=tokens_used
        )
        
        db.add(message)
        
        # Increment message count
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if session:
            session.message_count += 1
        
        db.commit()
        db.refresh(message)
        
        return message
    
    @staticmethod
    def get_session_messages(
        db: Session,
        session_id: uuid.UUID,
        limit: int | None = None
    ) -> list[Message]:
        """
        Get messages from session
        
        Args:
            session_id: Session UUID
            limit: Max number of recent messages to return (None = all)
        """
        query = db.query(Message).filter(
            Message.session_id == session_id
        ).order_by(Message.timestamp.desc())
        
        if limit:
            query = query.limit(limit)
        
        messages = query.all()
        return list(reversed(messages))  # Return in chronological order
    
    @staticmethod
    def get_session_info(db: Session, session_id: uuid.UUID) -> dict:
        """Get session information"""
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        
        if not session:
            return None
        
        now = datetime.now(timezone.utc)
        time_remaining = session.expires_at - now
        
        return {
            "session_id": str(session.id),
            "session_date": session.session_date.isoformat(),
            "started_at": session.started_at.isoformat(),
            "expires_at": session.expires_at.isoformat(),
            "time_remaining_hours": time_remaining.total_seconds() / 3600,
            "message_count": session.message_count,
            "is_active": session.is_active,
            "is_expired": session.expires_at <= now
        }
    
    @staticmethod
    def cleanup_old_sessions(db: Session, days_to_keep: int = 7):
        """
        Clean up old sessions
        Keep only recent sessions (default: last 7 days)
        """
        cutoff_date = date.today() - timedelta(days=days_to_keep)
        
        # Delete old sessions (cascade will delete messages too)
        deleted = db.query(ChatSession).filter(
            ChatSession.session_date < cutoff_date
        ).delete()
        
        db.commit()
        
        return deleted
