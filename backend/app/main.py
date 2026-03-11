from fastapi import FastAPI, HTTPException, Depends
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

# Initialize FastAPI app
app = FastAPI(
    title="AiKO API",
    description="Backend API for AiKO - AI Companion",
    version="0.1.0"
)

# CORS middleware (Allow all origins for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "AiKO API is running! 💕",
        "version": "0.1.0"
    }

@app.get("/test-chat", response_class=HTMLResponse)
async def test_chat():
    """Serve HTML test chat interface"""
    html_path = Path(__file__).parent.parent / "static" / "index.html"
    if html_path.exists():
        return html_path.read_text(encoding="utf-8")
    return "<h1>Chat interface not found</h1>"

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Chat endpoint with Aiko
    
    Handles:
    1. Web launcher commands
    2. Regular conversation with session management
    """
    try:
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
                    username=request.user_id or "default_user"
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
            username=request.user_id or "default_user",
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

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint
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

@app.get("/session/info")
async def get_session_info(
    username: str = "default_user",
    db: Session = Depends(get_db)
):
    """Get current session information"""
    try:
        info = chat_service.get_session_info(db, username)
        return {
            "status": "success",
            "data": info
        }
    except Exception as e:
        print(f"Error getting session info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/session/history")
async def get_chat_history(
    username: str = "default_user",
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get chat history for current session"""
    try:
        history = chat_service.get_chat_history(db, username, limit)
        return {
            "status": "success",
            "count": len(history),
            "messages": history
        }
    except Exception as e:
        print(f"Error getting chat history: {e}")
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