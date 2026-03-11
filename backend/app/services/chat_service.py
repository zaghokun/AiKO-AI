"""
Chat service - orchestrates Gemini + Database + Session management + RAG Memory
"""

from sqlalchemy.orm import Session
from .gemini_service import GeminiService
from .memory_service import memory_service
from ..database import SessionManager
from ..models import ChatMessage

class ChatService:
    """High-level chat service with RAG memory"""
    
    def __init__(self):
        self.gemini = GeminiService()
    
    def chat(
        self,
        db: Session,
        user_message: str,
        username: str = "default_user",
        context_limit: int = 20,
        use_rag: bool = True
    ) -> dict:
        """
        Process chat message with session management and RAG memory
        
        Args:
            db: Database session
            user_message: User's message
            username: Username for session
            context_limit: Number of recent messages to include as context
            use_rag: Whether to use RAG semantic search
            
        Returns:
            dict with response, session_info, etc.
        """
        # Get or create session
        session = SessionManager.get_or_create_session(db, username)
        user = session.user
        
        # Check message limit
        if session.message_count >= 100:  # safety limit
            return {
                "response": "Aduh, udah terlalu banyak pesan hari ini... 😅 Istirahat dulu yuk! Besok kita lanjut ngobrol lagi ya~ 💕",
                "action": "limit_reached",
                "session_info": SessionManager.get_session_info(db, session.id)
            }
        
        # Build context with RAG
        recent_messages, relevant_memories = memory_service.build_context_with_memory(
            db=db,
            user_message=user_message,
            session_id=str(session.id),
            user_id=str(user.id),
            recent_message_limit=context_limit,
            use_semantic_search=use_rag
        )
        
        # Format memory context for LLM if we have relevant memories
        memory_context = None
        if relevant_memories:
            memory_context = memory_service.format_memory_context(relevant_memories)
            print(f"🧠 Found {len(relevant_memories)} relevant memories")
        
        # Get response from Gemini with memory context
        if memory_context:
            # Inject memory context into system
            aiko_response = self.gemini.chat_with_memory(
                message=user_message,
                history=recent_messages,
                memory_context=memory_context
            )
        else:
            # Regular chat without long-term memory
            aiko_response = self.gemini.chat(user_message, recent_messages)
        
        # Save user message to PostgreSQL
        user_msg = SessionManager.add_message(
            db,
            session.id,
            role="user",
            content=user_message
        )
        
        # Save assistant response to PostgreSQL
        assistant_msg = SessionManager.add_message(
            db,
            session.id,
            role="assistant",
            content=aiko_response
        )
        
        # Save both messages to Qdrant for semantic search
        try:
            memory_service.save_message_to_vector_db(
                user_msg,
                user_id=str(user.id),
                session_id=str(session.id)
            )
            memory_service.save_message_to_vector_db(
                assistant_msg,
                user_id=str(user.id),
                session_id=str(session.id)
            )
        except Exception as e:
            print(f"⚠️  Warning: Could not save to vector DB: {e}")
        
        return {
            "response": aiko_response,
            "action": None,
            "session_info": SessionManager.get_session_info(db, session.id),
            "message_count": session.message_count,
            "memories_used": len(relevant_memories) if relevant_memories else 0
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
