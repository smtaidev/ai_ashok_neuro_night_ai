from pydantic import BaseModel
from typing import List, Dict, Optional

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    message: str

class ChatbotRequest(BaseModel):
    message: str
    session_id: Optional[str] = None  # Optional session ID for user tracking
    history: Optional[List[Dict]] = []

class ChatbotResponse(BaseModel):
    response: str