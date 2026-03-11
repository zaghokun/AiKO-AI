"""
Qdrant service for vector database operations
Handles memory storage and semantic search
"""

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    SearchRequest
)
from typing import List, Dict, Optional
import uuid
from datetime import datetime
from ..config import settings
from .embedding_service import embedding_service

class QdrantService:
    """Service for Qdrant vector database operations"""
    
    def __init__(self):
        """Initialize Qdrant client"""
        self.client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port
        )
        self.collection_name = settings.qdrant_collection_name
        self._ensure_collection()
    
    def _ensure_collection(self):
        """Create collection if it doesn't exist"""
        try:
            # Check if collection exists
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]
            
            if self.collection_name not in collection_names:
                print(f"🔄 Creating Qdrant collection: {self.collection_name}")
                
                # Create collection with vector config
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=embedding_service.get_dimension(),
                        distance=Distance.COSINE
                    )
                )
                
                print(f"✅ Collection created!")
            else:
                print(f"✅ Qdrant collection ready: {self.collection_name}")
                
        except Exception as e:
            print(f"⚠️  Qdrant collection setup warning: {e}")
    
    def add_memory(
        self,
        message_id: str,
        user_id: str,
        session_id: str,
        role: str,
        content: str,
        timestamp: datetime,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Add a message to vector memory
        
        Args:
            message_id: Unique message ID
            user_id: User ID
            session_id: Session ID
            role: Message role (user/assistant)
            content: Message content
            timestamp: Message timestamp
            metadata: Additional metadata
            
        Returns:
            True if successful
        """
        try:
            # Generate embedding
            embedding = embedding_service.encode(content)
            
            # Prepare payload
            payload = {
                "message_id": message_id,
                "user_id": user_id,
                "session_id": session_id,
                "role": role,
                "content": content,
                "timestamp": timestamp.isoformat(),
                **(metadata or {})
            }
            
            # Create point
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload=payload
            )
            
            # Upsert to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            
            return True
            
        except Exception as e:
            print(f"❌ Error adding memory to Qdrant: {e}")
            return False
    
    def search_memories(
        self,
        query: str,
        user_id: str,
        limit: int = 5,
        score_threshold: float = 0.7,
        exclude_session_id: Optional[str] = None
    ) -> List[Dict]:
        """
        Search for relevant memories using semantic search
        
        Args:
            query: Search query text
            user_id: User ID to filter by
            limit: Max number of results
            score_threshold: Minimum similarity score (0-1)
            exclude_session_id: Exclude memories from this session
            
        Returns:
            List of relevant memories with scores
        """
        try:
            # Generate query embedding
            query_embedding = embedding_service.encode(query)
            
            # Build filter for user
            filter_conditions = [
                FieldCondition(
                    key="user_id",
                    match=MatchValue(value=user_id)
                )
            ]
            
            # Search in Qdrant
            search_result = self.client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                query_filter=Filter(must=filter_conditions) if filter_conditions else None,
                limit=limit,
                score_threshold=score_threshold
            ).points
            
            # Format results
            memories = []
            for hit in search_result:
                memory = {
                    "content": hit.payload.get("content"),
                    "role": hit.payload.get("role"),
                    "timestamp": hit.payload.get("timestamp"),
                    "session_id": hit.payload.get("session_id"),
                    "score": hit.score
                }
                
                # Exclude current session if specified
                if exclude_session_id and memory["session_id"] == exclude_session_id:
                    continue
                
                memories.append(memory)
            
            return memories[:limit]
            
        except Exception as e:
            print(f"❌ Error searching memories: {e}")
            return []
    
    def get_memory_count(self, user_id: Optional[str] = None) -> int:
        """
        Get total count of memories
        
        Args:
            user_id: Optional user ID to filter
            
        Returns:
            Number of memories
        """
        try:
            if user_id:
                # Count with filter
                result = self.client.scroll(
                    collection_name=self.collection_name,
                    scroll_filter=Filter(
                        must=[FieldCondition(
                            key="user_id",
                            match=MatchValue(value=user_id)
                        )]
                    ),
                    limit=1,
                    with_payload=False,
                    with_vectors=False
                )
                # This is approximate - for exact count would need to scroll all
                return len(result[0])
            else:
                # Get collection info
                collection_info = self.client.get_collection(self.collection_name)
                return collection_info.points_count
                
        except Exception as e:
            print(f"⚠️  Error getting memory count: {e}")
            return 0
    
    def delete_session_memories(self, session_id: str) -> bool:
        """
        Delete all memories from a specific session
        
        Args:
            session_id: Session ID
            
        Returns:
            True if successful
        """
        try:
            # Delete points matching session_id
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=Filter(
                    must=[FieldCondition(
                        key="session_id",
                        match=MatchValue(value=session_id)
                    )]
                )
            )
            return True
            
        except Exception as e:
            print(f"❌ Error deleting session memories: {e}")
            return False
    
    def delete_user_memories(self, user_id: str) -> bool:
        """
        Delete all memories for a user
        
        Args:
            user_id: User ID
            
        Returns:
            True if successful
        """
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=Filter(
                    must=[FieldCondition(
                        key="user_id",
                        match=MatchValue(value=user_id)
                    )]
                )
            )
            return True
            
        except Exception as e:
            print(f"❌ Error deleting user memories: {e}")
            return False

# Global instance
qdrant_service = QdrantService()
