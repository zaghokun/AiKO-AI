"""
Embedding service for converting text to vectors
Uses sentence-transformers for semantic embeddings
"""

from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
from ..config import settings

class EmbeddingService:
    """Service for generating text embeddings"""
    
    _instance = None
    _model = None
    
    def __new__(cls):
        """Singleton pattern - load model once"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize embedding model"""
        if self._model is None:
            print(f"🔄 Loading embedding model: {settings.embedding_model}")
            self._model = SentenceTransformer(settings.embedding_model)
            print(f"✅ Embedding model loaded! Dimension: {self.get_dimension()}")
    
    def get_dimension(self) -> int:
        """Get embedding dimension"""
        return self._model.get_sentence_embedding_dimension()
    
    def encode(self, text: str) -> List[float]:
        """
        Convert text to embedding vector
        
        Args:
            text: Input text
            
        Returns:
            List of floats (embedding vector)
        """
        if not text or not text.strip():
            # Return zero vector for empty text
            return [0.0] * self.get_dimension()
        
        embedding = self._model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True  # L2 normalization
        )
        
        return embedding.tolist()
    
    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Convert multiple texts to embeddings (batch processing)
        
        Args:
            texts: List of input texts
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        # Filter empty texts
        valid_texts = [text if text and text.strip() else " " for text in texts]
        
        embeddings = self._model.encode(
            valid_texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            batch_size=32,
            show_progress_bar=False
        )
        
        return embeddings.tolist()
    
    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Compute cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score (0-1, higher = more similar)
        """
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        # Cosine similarity (already normalized, so just dot product)
        similarity = np.dot(vec1, vec2)
        
        return float(similarity)

# Global instance
embedding_service = EmbeddingService()
