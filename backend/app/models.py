from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ChatMessage(BaseModel):
    """Chat message model"""
    role: str = Field(..., description="Role: user or assistant")
    content: str = Field(..., description="Message content")

class ChatRequest(BaseModel):
    """Chat request from frontend"""
    message: str = Field(..., min_length=1, max_length=2000)
    history: Optional[List[ChatMessage]] = Field(default_factory=list)
    user_id: Optional[str] = None

class WebLauncherAction(BaseModel):
    """Web launcher action"""
    website: str
    url: str

class ChatResponse(BaseModel):
    """Chat response to frontend"""
    response: str
    action: Optional[str] = None
    action_data: Optional[Dict[str, Any]] = None
    message_id: Optional[str] = None