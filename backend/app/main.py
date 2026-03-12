from fastapi import FastAPI, HTTPException, Depends, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import uvicorn
import os
from pathlib import Path
from .config import settings
from .models import ChatRequest, ChatResponse
from .services import GeminiService, WebLauncherService, ChatService
from .database import get_db, init_db
from .database.models import User
from .routes.auth import router as auth_router
from .dependencies.auth import get_optional_current_user
from .websocket import websocket_endpoint, manager
from .middleware.security_headers import SecurityHeadersMiddleware
from typing import Optional

# Initialize FastAPI app
app = FastAPI(
    title="AiKO API",
    description="""
# AiKO - AI Companion API

Backend API for AiKO, your personal AI companion with Aiko personality.

## Features

* 🔐 **Authentication**: JWT-based user authentication
* 💬 **Chat**: Text & streaming chat with Aiko personality
* 🌐 **WebSocket**: Real-time bidirectional chat
* 🧠 **RAG Memory**: Semantic memory with Qdrant vector database
* 📝 **Session Management**: 24-hour chat sessions with context
* 🚀 **Web Launcher**: Open websites via chat commands
* 🛡️ **Security**: Rate limiting, input sanitization, security headers

## Authentication

Most endpoints support optional authentication. Use the 🔓 Authorize button with your JWT token.

1. **Register** a new account at `/auth/register`
2. **Login** to get JWT token at `/auth/login`
3. Click 🔓 **Authorize** and paste your token
4. Now you have personal memory and chat history!

## WebSocket Connection

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat?token=YOUR_JWT_TOKEN');
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log(data);
};
ws.send(JSON.stringify({type: 'message', content: 'Hello Aiko!'}));
```

## Rate Limits

- **REST API**: 100 requests per hour per user/IP
- **WebSocket**: 30 messages per minute per user

---
Made with 💕 by the AiKO team
    """,
    version="0.2.0",
    contact={
        "name": "AiKO Team",
        "url": "https://github.com/yourusername/aiko-ai"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_tags=[
        {
            "name": "Health",
            "description": "API health check and status"
        },
        {
            "name": "Authentication",
            "description": "User registration, login, and profile management"
        },
        {
            "name": "Chat",
            "description": "Chat with Aiko using text or streaming responses"
        },
        {
            "name": "WebSocket",
            "description": "Real-time bidirectional chat via WebSocket"
        },
        {
            "name": "Session",
            "description": "Chat session and history management"
        },
        {
            "name": "Memory",
            "description": "Semantic memory search and statistics"
        }
    ]
)

# Add security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# CORS middleware (Allow all origins for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)

# Mount static files
static_path = Path(__file__).parent.parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Initialize services
gemini_service = GeminiService()
web_launcher = WebLauncherService()
chat_service = ChatService()

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        init_db()
        print("✅ Database initialized!")
    except Exception as e:
        print(f"⚠️  Database initialization warning: {e}")

@app.get("/", tags=["Health"])
async def root():
    """
    Health check endpoint
    
    Returns API status, version, and available features.
    """
    return {
        "status": "ok",
        "message": "AiKO API is running! 💕",
        "version": "0.2.0",
        "features": ["REST API", "WebSocket", "Authentication", "RAG Memory"]
    }


# WebSocket endpoint
@app.websocket("/ws/chat")
async def websocket_chat_endpoint(
    websocket: WebSocket,
    db: Session = Depends(get_db)
):
    """
    WebSocket endpoint for real-time chat
    
    Connection: ws://localhost:8000/ws/chat?token=YOUR_JWT_TOKEN
    
    Supports:
    - Real-time messaging
    - Streaming responses
    - Typing indicators
    - Auto-save to database
    """
    await websocket_endpoint(websocket, db)


@app.get("/ws/active-users", tags=["WebSocket"])
async def get_active_users():
    """
    Get list of active WebSocket users
    
    Returns all currently connected users with their connection timestamps.
    """
    return {
        "status": "success",
        "count": len(manager.active_connections),
        "users": manager.get_active_users()
    }


@app.get("/test-chat", response_class=HTMLResponse)
async def test_chat():
    """Serve HTML test chat interface"""
    html_path = Path(__file__).parent.parent / "static" / "index.html"
    if html_path.exists():
        return html_path.read_text(encoding="utf-8")
    return "<h1>Chat interface not found</h1>"

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Chat with Aiko (non-streaming)
    
    Supports both authenticated and guest users:
    - **Authenticated**: Uses your personal memory and history
    - **Guest**: Uses default_user account
    
    Features:
    - 🌐 Web launcher commands ("buka YouTube", "open Google")
    - 💬 Natural conversation with Aiko personality
    - 🧠 RAG-enhanced responses using semantic memory
    - 📝 Auto-save to 24-hour sessions
    
    Example:
    ```json
    {
      "message": "Hai Aiko! Apa kabar?",
      "user_id": "optional_user_id",
      "history": []
    }
    ```
    """
    try:
        # Determine username (authenticated user or guest)
        if current_user:
            username = current_user.username
        else:
            username = request.user_id or "default_user"
        
        # Check for web launcher command
        website_data = web_launcher.detect_website(request.message)
        
        if website_data:
            # Launch website
            success = web_launcher.launch(website_data["url"])
            
            if success:
                # Get Aiko's response
                aiko_response = web_launcher.get_response_message(website_data["website"])
                
                # Save to database
                result = chat_service.chat(
                    db=db,
                    user_message=request.message,
                    username=username  # Use determined username
                )
                
                return ChatResponse(
                    response=aiko_response,
                    action="open_website",
                    action_data=website_data
                )
            else:
                return ChatResponse(
                    response="Aduh, maaf ya... Aku ga bisa buka websitenya 😅",
                    action="error"
                )
        
        # Regular chat with session management
        result = chat_service.chat(
            db=db,
            user_message=request.message,
            username=username,  # Use determined username
            context_limit=20
        )
        
        return ChatResponse(
            response=result["response"],
            action=result.get("action"),
            action_data=result.get("session_info")
        )
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

@app.post("/chat/stream", tags=["Chat"])
async def chat_stream(request: ChatRequest):
    """
    Streaming chat with Aiko
    
    Returns Server-Sent Events (SSE) stream for real-time responses.
    
    Each chunk is sent as:
    ```
    data: word
    data: [DONE]
    ```
    
    Use this for typewriter effect in UI.
    """
    try:
        # Check for web launcher first
        website_data = web_launcher.detect_website(request.message)
        
        if website_data:
            # For web launcher, return immediately (no streaming needed)
            web_launcher.launch(website_data["url"])
            response_text = web_launcher.get_response_message(website_data["website"])
            
            async def generate():
                yield f"data: {response_text}\n\n"
                yield "data: [DONE]\n\n"
            
            return StreamingResponse(
                generate(),
                media_type="text/event-stream"
            )
        
        # Stream regular chat
        async def generate():
            async for chunk in gemini_service.chat_stream(
                message=request.message,
                history=request.history
            ):
                yield f"data: {chunk}\n\n"
            yield "data: [DONE]\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream"
        )
        
    except Exception as e:
        print(f"Error in stream endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

@app.get("/session/info", tags=["Session"])
async def get_session_info(
    username: str = "default_user",
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Get current session information
    
    Returns:
    - Session ID and creation time
    - Expiration timestamp (24h from creation)
    - Total messages in session
    - Whether session is active
    
    Supports authentication - uses your username if logged in.
    """
    try:
        # Use authenticated user if available
        actual_username = current_user.username if current_user else username
        info = chat_service.get_session_info(db, actual_username)
        return {
            "status": "success",
            "data": info
        }
    except Exception as e:
        print(f"Error getting session info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/session/history", tags=["Session"])
async def get_chat_history(
    username: str = "default_user",
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Get chat history for current session
    
    Returns the most recent messages from your active 24-hour session.
    
    **Parameters:**
    - **limit**: Maximum number of messages to return (default: 50)
    - **username**: Username (ignored if authenticated)
    
    Supports authentication - uses your username if logged in.
    """
    try:
        # Use authenticated user if available
        actual_username = current_user.username if current_user else username
        history = chat_service.get_chat_history(db, actual_username, limit)
        return {
            "status": "success",
            "count": len(history),
            "messages": history
        }
    except Exception as e:
        print(f"Error getting chat history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memory/stats", tags=["Memory"])
async def get_memory_stats(
    username: str = "default_user",
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Get semantic memory statistics
    
    Returns:
    - Total memories stored in vector database
    - Memory collection info from Qdrant
    - User-specific memory count
    
    Supports authentication - uses your user ID if logged in.
    """
    try:
        from .services import memory_service
        from .database import SessionManager
        
        # Use authenticated user if available
        if current_user:
            user = current_user
        else:
            # Get or create user
            user = SessionManager.get_or_create_user(db, username)
        
        stats = memory_service.get_memory_stats(str(user.id))
        return {
            "status": "success",
            "data": stats
        }
    except Exception as e:
        print(f"Error getting memory stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/memory/search", tags=["Memory"])
async def search_memories(
    query: str,
    username: str = "default_user",
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Search for relevant semantic memories
    
    Uses vector similarity search to find relevant past conversations.
    
    **Parameters:**
    - **query**: Search query text
    - **limit**: Maximum memories to return (default: 5)
    - **username**: Username (ignored if authenticated)
    
    Returns memories with similarity scores (0.0 - 1.0).
    """
    try:
        from .services import memory_service
        from .database import SessionManager
        
        # Use authenticated user if available
        if current_user:
            user = current_user
            session = SessionManager.get_or_create_session(db, current_user.username)
        else:
            # Get user and session
            session = SessionManager.get_or_create_session(db, username)
            user = session.user
        
        memories = memory_service.get_relevant_memories(
            query=query,
            user_id=str(user.id),
            current_session_id=str(session.id),
            limit=limit
        )
        
        return {
            "status": "success",
            "query": query,
            "count": len(memories),
            "memories": memories
        }
    except Exception as e:
        print(f"Error searching memories: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
async def test_gemini():
    """Test Gemini API connection"""
    try:
        response = gemini_service.chat("Halo Aiko!")
        return {
            "status": "success",
            "response": response
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )