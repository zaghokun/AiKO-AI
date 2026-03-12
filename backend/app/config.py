from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings"""
    
    # API
    gemini_api_key: str
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # CORS
    allowed_origins: str = "http://localhost:3000,http://localhost:8000"
    
    # Database
    database_url: str = "postgresql://aiko_user:aiko_password_2026@localhost:5432/aiko_db"
    db_echo: bool = False
    
    # Session
    session_duration_hours: int = 24
    max_messages_per_session: int = 100
    
    # Authentication
    jwt_secret_key: str = "your-secret-key-change-in-production-min-32-chars"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # Qdrant Vector Database
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection_name: str = "aiko_memories"
    
    # RAG Configuration
    embedding_model: str = "all-MiniLM-L6-v2"
    memory_search_limit: int = 5
    memory_relevance_threshold: float = 0.7
    
    # Security & Rate Limiting
    rate_limit_requests: int = 100  # Max requests per window
    rate_limit_window_seconds: int = 3600  # 1 hour window
    websocket_rate_limit_messages: int = 30  # Max messages per minute
    websocket_rate_limit_window: int = 60  # 1 minute window
    max_message_length: int = 5000
    enable_security_headers: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings():
    """Get cached settings instance"""
    return Settings()

settings = get_settings()