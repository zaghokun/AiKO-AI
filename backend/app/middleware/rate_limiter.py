"""
Rate limiting middleware for API endpoints
Prevents abuse and DDoS attacks
"""

from fastapi import Request, HTTPException
from typing import Callable, Dict
import time
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    """
    Simple in-memory rate limiter
    For production, consider using Redis-based rate limiting
    """
    
    def __init__(self):
        # Store: {key: [(timestamp, count), ...]}
        self.requests: Dict[str, list] = defaultdict(list)
        self.cleanup_interval = 60  # Clean up old entries every 60 seconds
        self.last_cleanup = time.time()
    
    def _cleanup(self):
        """Remove old entries to prevent memory bloat"""
        current_time = time.time()
        if current_time - self.last_cleanup > self.cleanup_interval:
            cutoff_time = current_time - 3600  # Keep last hour
            for key in list(self.requests.keys()):
                self.requests[key] = [
                    (ts, count) for ts, count in self.requests[key]
                    if ts > cutoff_time
                ]
                if not self.requests[key]:
                    del self.requests[key]
            self.last_cleanup = current_time
    
    def _get_identifier(self, request: Request) -> str:
        """Get unique identifier for rate limiting"""
        # Try to get user from auth, fallback to IP
        user_id = None
        
        # Check if user is authenticated
        if hasattr(request.state, "user") and request.state.user:
            user_id = str(request.state.user.id)
        
        # Fallback to IP address
        if not user_id:
            forwarded = request.headers.get("X-Forwarded-For")
            if forwarded:
                user_id = forwarded.split(",")[0].strip()
            else:
                user_id = request.client.host if request.client else "unknown"
        
        return user_id
    
    def check_rate_limit(
        self,
        request: Request,
        max_requests: int,
        window_seconds: int
    ) -> tuple[bool, dict]:
        """
        Check if request exceeds rate limit
        
        Args:
            request: FastAPI request object
            max_requests: Maximum number of requests allowed
            window_seconds: Time window in seconds
            
        Returns:
            (allowed: bool, info: dict)
        """
        self._cleanup()
        
        identifier = self._get_identifier(request)
        current_time = time.time()
        window_start = current_time - window_seconds
        
        # Get requests within the time window
        recent_requests = [
            (ts, count) for ts, count in self.requests[identifier]
            if ts > window_start
        ]
        
        # Calculate total requests in window
        total_requests = sum(count for _, count in recent_requests)
        
        if total_requests >= max_requests:
            # Rate limit exceeded
            oldest_request = min(ts for ts, _ in recent_requests) if recent_requests else current_time
            retry_after = int(window_seconds - (current_time - oldest_request))
            
            return False, {
                "allowed": False,
                "limit": max_requests,
                "remaining": 0,
                "reset": int(current_time + retry_after),
                "retry_after": retry_after
            }
        
        # Add current request
        self.requests[identifier].append((current_time, 1))
        
        return True, {
            "allowed": True,
            "limit": max_requests,
            "remaining": max_requests - total_requests - 1,
            "reset": int(current_time + window_seconds)
        }


# Global rate limiter instance
rate_limiter = RateLimiter()


def rate_limit(max_requests: int = 100, window_seconds: int = 3600):
    """
    Rate limit decorator for endpoints
    
    Args:
        max_requests: Maximum requests allowed in window
        window_seconds: Time window in seconds
        
    Example:
        @app.get("/api/endpoint")
        @rate_limit(max_requests=10, window_seconds=60)
        async def my_endpoint():
            return {"message": "success"}
    """
    def decorator(func: Callable):
        async def wrapper(request: Request, *args, **kwargs):
            allowed, info = rate_limiter.check_rate_limit(
                request, max_requests, window_seconds
            )
            
            if not allowed:
                raise HTTPException(
                    status_code=429,
                    detail={
                        "error": "Rate limit exceeded",
                        "message": f"Too many requests. Try again in {info['retry_after']} seconds.",
                        "limit": info["limit"],
                        "retry_after": info["retry_after"]
                    },
                    headers={
                        "X-RateLimit-Limit": str(info["limit"]),
                        "X-RateLimit-Remaining": str(info["remaining"]),
                        "X-RateLimit-Reset": str(info["reset"]),
                        "Retry-After": str(info["retry_after"])
                    }
                )
            
            return await func(request, *args, **kwargs)
        
        wrapper.__name__ = func.__name__
        return wrapper
    
    return decorator


class WebSocketRateLimiter:
    """Rate limiter specifically for WebSocket messages"""
    
    def __init__(self):
        # Store: {user_id: [(timestamp, 1), ...]}
        self.messages: Dict[str, list] = defaultdict(list)
    
    def check_message_rate(
        self,
        user_id: str,
        max_messages: int = 30,
        window_seconds: int = 60
    ) -> tuple[bool, int]:
        """
        Check if user exceeds message rate limit
        
        Args:
            user_id: User identifier
            max_messages: Max messages allowed in window
            window_seconds: Time window in seconds
            
        Returns:
            (allowed: bool, remaining: int)
        """
        current_time = time.time()
        window_start = current_time - window_seconds
        
        # Filter messages within window
        self.messages[user_id] = [
            ts for ts in self.messages[user_id]
            if ts > window_start
        ]
        
        message_count = len(self.messages[user_id])
        
        if message_count >= max_messages:
            return False, 0
        
        # Add current message timestamp
        self.messages[user_id].append(current_time)
        
        return True, max_messages - message_count - 1


# Global WebSocket rate limiter
ws_rate_limiter = WebSocketRateLimiter()
