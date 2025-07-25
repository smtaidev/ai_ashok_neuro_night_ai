from fastapi import APIRouter, HTTPException
from app.services.chat_manager import ChatManager
from app.api.models.chat_model import ChatbotRequest, ChatbotResponse
import uuid

router = APIRouter()

# Initialize chat manager
chat_manager = ChatManager()

# New chatbot endpoint
@router.post("/chatbot", response_model=ChatbotResponse)
async def chatbot_endpoint(request: ChatbotRequest):
    try:
        # Generate a session ID (you might want to pass this from frontend)
        session_id = "default_session"  # In production, use proper session management
        
        response = await chat_manager.chat(
            user_id=session_id,
            prompt=request.message,
            chat_history=request.history
        )
        
        return ChatbotResponse(response=response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.post("/chatbot/clear")
async def clear_chat_history():
    try:
        session_id = "default_session"
        success = chat_manager.clear_chat_history(session_id)
        return {"success": success, "message": "Chat history cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")