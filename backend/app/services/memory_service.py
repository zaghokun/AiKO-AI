"""
Memory service - RAG orchestration
Combines recent context + semantic search for enhanced memory
"""

from sqlalchemy.orm import Session
from typing import List, Dict
from ..database import SessionManager, Message
from ..models import ChatMessage
from .qdrant_service import qdrant_service
from ..config import settings

class MemoryService:
    """Service for managing conversation memory with RAG"""
    
    @staticmethod
    def save_message_to_vector_db(
        message: Message,
        user_id: str,
        session_id: str
    ) -> bool:
        """
        Save message to Qdrant vector database
        
        Args:
            message: Message object from PostgreSQL
            user_id: User ID
            session_id: Session ID
            
        Returns:
            True if successful
        """
        return qdrant_service.add_memory(
            message_id=str(message.id),
            user_id=user_id,
            session_id=session_id,
            role=message.role,
            content=message.content,
            timestamp=message.timestamp
        )
    
    @staticmethod
    def get_relevant_memories(
        query: str,
        user_id: str,
        current_session_id: str,
        limit: int = None,
        threshold: float = None
    ) -> List[Dict]:
        """
        Search for relevant past memories using semantic search
        
        Args:
            query: Search query (user's message)
            user_id: User ID
            current_session_id: Current session ID (to exclude recent messages)
            limit: Max results (default from config)
            threshold: Min similarity score (default from config)
            
        Returns:
            List of relevant memories
        """
        limit = limit or settings.memory_search_limit
        threshold = threshold or settings.memory_relevance_threshold
        
        return qdrant_service.search_memories(
            query=query,
            user_id=user_id,
            limit=limit,
            score_threshold=threshold,
            exclude_session_id=current_session_id
        )
    
    @staticmethod
    def build_context_with_memory(
        db: Session,
        user_message: str,
        session_id: str,
        user_id: str,
        recent_message_limit: int = 20,
        use_semantic_search: bool = True
    ) -> tuple[List[ChatMessage], List[Dict]]:
        """
        Build conversation context with RAG
        Combines recent messages + semantically relevant past memories
        
        Args:
            db: Database session
            user_message: Current user message
            session_id: Current session ID
            user_id: User ID
            recent_message_limit: Number of recent messages to include
            use_semantic_search: Whether to use semantic search
            
        Returns:
            Tuple of (recent_messages, relevant_memories)
        """
        # 1. Get recent messages from current session (PostgreSQL)
        recent_db_messages = SessionManager.get_session_messages(
            db,
            session_id,
            limit=recent_message_limit
        )
        
        # Convert to ChatMessage format
        recent_messages = [
            ChatMessage(role=msg.role, content=msg.content)
            for msg in recent_db_messages
        ]
        
        # 2. Get semantically relevant memories from past (Qdrant)
        relevant_memories = []
        if use_semantic_search:
            relevant_memories = MemoryService.get_relevant_memories(
                query=user_message,
                user_id=user_id,
                current_session_id=session_id
            )
        
        return recent_messages, relevant_memories
    
    @staticmethod
    def format_memory_context(memories: List[Dict]) -> str:
        """
        Format relevant memories into a context string for the LLM
        
        Args:
            memories: List of memory dictionaries
            
        Returns:
            Formatted context string
        """
        if not memories:
            return ""
        
        context_parts = ["[Relevant past conversations:]"]
        
        for i, memory in enumerate(memories, 1):
            role = "User" if memory["role"] == "user" else "Aiko"
            content = memory["content"]
            score = memory.get("score", 0)
            
            # Truncate long memories
            if len(content) > 200:
                content = content[:197] + "..."
            
            context_parts.append(f"{i}. {role}: {content} (relevance: {score:.2f})")
        
        context_parts.append("[End of past conversations]")
        context_parts.append("")
        
        return "\n".join(context_parts)
    
    @staticmethod
    def get_memory_stats(user_id: str) -> Dict:
        """
        Get memory statistics for a user
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with stats
        """
        total_memories = qdrant_service.get_memory_count(user_id)
        
        return {
            "total_memories": total_memories,
            "vector_dimension": settings.embedding_model,
            "search_limit": settings.memory_search_limit,
            "relevance_threshold": settings.memory_relevance_threshold
        }

# Global instance
memory_service = MemoryService()
