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
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings():
    """Get cached settings instance"""
    return Settings()

settings = get_settings()