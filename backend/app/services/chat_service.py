"""
Chat service - orchestrates Gemini + Database + Session management
"""

from sqlalchemy.orm import Session
from .gemini_service import GeminiService
from ..database import SessionManager
from ..models import ChatMessage

class ChatService:
    """High-level chat service"""
    
    def __init__(self):
        self.gemini = GeminiService()
    
    def chat(
        self,
        db: Session,
        user_message: str,
        username: str = "default_user",
        context_limit: int = 20
    ) -> dict:
        """
        Process chat message with session management
        
        Args:
            db: Database session
            user_message: User's message
            username: Username for session
            context_limit: Number of recent messages to include as context
            
        Returns:
            dict with response, session_info, etc.
        """
        # Get or create session
        session = SessionManager.get_or_create_session(db, username)
        
        # Check message limit
        if session.message_count >= 100:  # safety limit
            return {
                "response": "Aduh, udah terlalu banyak pesan hari ini... 😅 Istirahat dulu yuk! Besok kita lanjut ngobrol lagi ya~ 💕",
                "action": "limit_reached",
                "session_info": SessionManager.get_session_info(db, session.id)
            }
        
        # Get recent messages for context
        recent_messages = SessionManager.get_session_messages(
            db,
            session.id,
            limit=context_limit
        )
        
        # Convert to ChatMessage format for Gemini
        history = [
            ChatMessage(role=msg.role, content=msg.content)
            for msg in recent_messages
        ]
        
        # Get response from Gemini
        aiko_response = self.gemini.chat(user_message, history)
        
        # Save user message
        SessionManager.add_message(
            db,
            session.id,
            role="user",
            content=user_message
        )
        
        # Save assistant response
        SessionManager.add_message(
            db,
            session.id,
            role="assistant",
            content=aiko_response
        )
        
        return {
            "response": aiko_response,
            "action": None,
            "session_info": SessionManager.get_session_info(db, session.id),
            "message_count": session.message_count + 2  # +2 for the messages we just added
        }
    
    def get_chat_history(
        self,
        db: Session,
        username: str = "default_user",
        limit: int | None = 50
    ) -> list[dict]:
        """Get chat history for user's current session"""
        # Get or create session
        session = SessionManager.get_or_create_session(db, username)
        
        # Get messages
        messages = SessionManager.get_session_messages(db, session.id, limit)
        
        return [msg.to_dict() for msg in messages]
    
    def get_session_info(
        self,
        db: Session,
        username: str = "default_user"
    ) -> dict:
        """Get current session information"""
        session = SessionManager.get_or_create_session(db, username)
        return SessionManager.get_session_info(db, session.id)
