"""
Authentication dependencies and middleware
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from ..database.connection import get_db
from ..database.models import User
from ..services.auth_service import auth_service
from ..schemas.auth import TokenData

# Security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token
    
    Args:
        credentials: HTTP Bearer token
        db: Database session
        
    Returns:
        User object
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verify token
    token = credentials.credentials
    payload = auth_service.verify_token(token)
    
    if payload is None:
        raise credentials_exception
    
    # Extract user info
    user_id: str = payload.get("user_id")
    username: str = payload.get("username")
    
    if user_id is None or username is None:
        raise credentials_exception
    
    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user
    
    Args:
        current_user: User from get_current_user
        
    Returns:
        User object
        
    Raises:
        HTTPException: If user is not active
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get current user if authenticated, otherwise None
    Useful for optional authentication
    
    Args:
        credentials: HTTP Bearer token (optional)
        db: Database session
        
    Returns:
        User object or None
    """
    if credentials is None:
        return None
    
    try:
        token = credentials.credentials
        payload = auth_service.verify_token(token)
        
        if payload is None:
            return None
        
        user_id = payload.get("user_id")
        if user_id is None:
            return None
        
        user = db.query(User).filter(User.id == user_id).first()
        return user if user and user.is_active else None
        
    except Exception:
        return None
