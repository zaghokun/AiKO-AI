"""
Authentication schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserRegister(BaseModel):
    """User registration request"""
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_-]+$")
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    """User login request"""
    username: str
    password: str


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class TokenData(BaseModel):
    """Data stored in JWT token"""
    user_id: str
    username: str


class UserResponse(BaseModel):
    """User data response"""
    id: UUID
    username: str
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    """User profile with stats"""
    id: UUID
    username: str
    email: str
    is_active: bool
    created_at: datetime
    total_sessions: int = 0
    total_messages: int = 0
    total_memories: int = 0
