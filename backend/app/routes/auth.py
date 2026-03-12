"""
Authentication routes
Handles user registration, login, and profile
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database.connection import get_db
from ..database.models import User, ChatSession, Message
from ..schemas.auth import (
    UserRegister,
    UserLogin,
    Token,
    UserResponse,
    UserProfile
)
from ..services.auth_service import auth_service
from ..services.memory_service import MemoryService
from ..dependencies.auth import get_current_user, get_current_active_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    
    - **username**: Unique username (3-50 chars, alphanumeric, underscore, dash)
    - **email**: Valid email address
    - **password**: Password (min 8 chars)
    """
    # Check if username exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = auth_service.hash_password(user_data.password)
    
    # Create user
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=Token)
async def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login with username and password
    
    Returns JWT access token
    """
    # Find user
    user = db.query(User).filter(User.username == user_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not auth_service.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    # Create access token
    token_data = {
        "user_id": str(user.id),
        "username": user.username
    }
    
    access_token = auth_service.create_access_token(token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 86400  # 24 hours in seconds
    }


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user information
    
    Requires authentication token
    """
    return current_user


@router.get("/profile", response_model=UserProfile)
async def get_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get user profile with statistics
    
    Requires authentication token
    """
    # Get session count
    total_sessions = db.query(func.count(ChatSession.id)).filter(
        ChatSession.user_id == current_user.id
    ).scalar() or 0
    
    # Get message count
    total_messages = db.query(func.count(Message.id)).join(ChatSession).filter(
        ChatSession.user_id == current_user.id
    ).scalar() or 0
    
    # Get memory count
    total_memories = MemoryService.get_memory_stats(str(current_user.id)).get("total_memories", 0)
    
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at,
        "total_sessions": total_sessions,
        "total_messages": total_messages,
        "total_memories": total_memories
    }


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_active_user)
):
    """
    Logout current user
    
    Note: JWT tokens are stateless, so this is just a placeholder.
    Client should discard the token.
    """
    return {
        "status": "success",
        "message": "Logged out successfully. Please discard your token."
    }
