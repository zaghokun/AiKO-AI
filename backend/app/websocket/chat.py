"""
WebSocket chat endpoint
Real-time bidirectional chat with streaming responses
"""

from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import json
import asyncio

from .connection_manager import manager
from ..database.connection import get_db
from ..database.models import User
from ..services.auth_service import auth_service
from ..services.chat_service import ChatService
from ..services.gemini_service import GeminiService
from ..middleware.rate_limiter import ws_rate_limiter
from ..utils.sanitizer import sanitizer


async def authenticate_websocket(token: str, db: Session) -> Optional[User]:
    """
    Authenticate WebSocket connection via JWT token
    
    Args:
        token: JWT token
        db: Database session
        
    Returns:
        User object or None
    """
    try:
        # Verify token
        payload = auth_service.verify_token(token)
        
        if not payload:
            return None
        
        user_id = payload.get("user_id")
        if not user_id:
            return None
        
        # Get user from database
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user or not user.is_active:
            return None
        
        return user
        
    except Exception as e:
        print(f"WebSocket auth error: {e}")
        return None


async def websocket_endpoint(
    websocket: WebSocket,
    db: Session
):
    """
    WebSocket endpoint for real-time chat
    
    Connection URL: ws://localhost:8000/ws/chat?token=YOUR_JWT_TOKEN
    
    Message format (client -> server):
    {
        "type": "message",
        "content": "Your message here"
    }
    
    Message format (server -> client):
    {
        "type": "message" | "typing" | "error" | "system",
        "content": "Response message",
        "timestamp": "ISO timestamp"
    }
    """
    # Extract token from query parameters
    query_params = dict(websocket.query_params)
    token = query_params.get("token")
    
    if not token:
        await websocket.close(code=1008, reason="Missing authentication token")
        return
    
    # Authenticate user
    user = await authenticate_websocket(token, db)
    
    if not user:
        await websocket.close(code=1008, reason="Authentication failed")
        return
    
    # Connect user
    await manager.connect(websocket, str(user.id), user.username)
    
    # Initialize services
    chat_service = ChatService()
    gemini_service = GeminiService()
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            try:
                message_data = json.loads(data)
            except json.JSONDecodeError:
                await manager.send_error("Invalid JSON format", str(user.id))
                continue
            
            message_type = message_data.get("type", "message")
            
            # Handle ping first (no content validation needed)
            if message_type == "ping":
                await manager.send_personal_message({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                }, str(user.id))
                continue
            
            content = message_data.get("content", "").strip()
            
            # Rate limiting check
            allowed, remaining = ws_rate_limiter.check_message_rate(
                str(user.id),
                max_messages=30,  # 30 messages per minute
                window_seconds=60
            )
            
            if not allowed:
                await manager.send_error(
                    "Rate limit exceeded. Please slow down!",
                    str(user.id)
                )
                continue
            
            # Sanitize input
            content = sanitizer.sanitize_chat_message(content)
            
            if not content:
                await manager.send_error("Empty message", str(user.id))
                continue
            
            # Check for malicious input
            if sanitizer.detect_xss(content) or sanitizer.detect_sql_injection(content):
                await manager.send_error(
                    "Invalid message content detected",
                    str(user.id)
                )
                print(f"⚠️ Suspicious input detected from user {user.username}: {content[:100]}")
                continue
            
            # Handle different message types
            if message_type == "message":
                # Send typing indicator
                await manager.send_typing_indicator(str(user.id), True)
                
                try:
                    # Process message with chat service (saves to DB)
                    result = chat_service.chat(
                        db=db,
                        user_message=content,
                        username=user.username,
                        context_limit=20
                    )
                    
                    # Stop typing indicator
                    await manager.send_typing_indicator(str(user.id), False)
                    
                    # Send response
                    response_message = {
                        "type": "message",
                        "role": "assistant",
                        "content": result["response"],
                        "timestamp": datetime.now().isoformat(),
                        "memories_used": result.get("memories_used", 0)
                    }
                    
                    await manager.send_personal_message(response_message, str(user.id))
                    
                except Exception as e:
                    print(f"Error processing message: {e}")
                    await manager.send_typing_indicator(str(user.id), False)
                    await manager.send_error(
                        "Sorry, ada error pas proses pesanmu 😅",
                        str(user.id)
                    )
            
            elif message_type == "stream":
                # Handle streaming response (word-by-word)
                await manager.send_typing_indicator(str(user.id), True)
                
                try:
                    # Get chat history for context
                    history = chat_service.get_chat_history(db, user.username, limit=20)
                    
                    # Convert to ChatMessage format
                    from ..models import ChatMessage
                    chat_history = [
                        ChatMessage(role=msg["role"], content=msg["content"])
                        for msg in history
                    ]
                    
                    # Stream response
                    full_response = ""
                    async for chunk in gemini_service.chat_stream(content, chat_history):
                        full_response += chunk
                        # Send chunk
                        await manager.send_personal_message({
                            "type": "stream_chunk",
                            "content": chunk,
                            "timestamp": datetime.now().isoformat()
                        }, str(user.id))
                        
                        # Small delay for smoother streaming
                        await asyncio.sleep(0.01)
                    
                    # Stop typing indicator
                    await manager.send_typing_indicator(str(user.id), False)
                    
                    # Send stream end
                    await manager.send_personal_message({
                        "type": "stream_end",
                        "timestamp": datetime.now().isoformat()
                    }, str(user.id))
                    
                    # Save to database
                    result = chat_service.chat(
                        db=db,
                        user_message=content,
                        username=user.username,
                        context_limit=20
                    )
                    
                except Exception as e:
                    print(f"Error streaming message: {e}")
                    await manager.send_typing_indicator(str(user.id), False)
                    await manager.send_error(
                        "Sorry, ada error pas streaming 😅",
                        str(user.id)
                    )
            
            else:
                await manager.send_error(
                    f"Unknown message type: {message_type}",
                    str(user.id)
                )
    
    except WebSocketDisconnect:
        await manager.disconnect(str(user.id))
    
    except Exception as e:
        print(f"WebSocket error for {user.username}: {e}")
        await manager.disconnect(str(user.id))
