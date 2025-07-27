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
        # Generate or use provided session ID
        session_id = request.session_id if hasattr(request, 'session_id') else str(uuid.uuid4())
        
        response = await chat_manager.chat(
            user_id=session_id,
            prompt=request.message,
            chat_history=request.history
        )
        
        return ChatbotResponse(response=response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.post("/chatbot/clear")
async def clear_chat_history(session_id: str = None):
    try:
        session_id = session_id or str(uuid.uuid4())
        success = chat_manager.clear_chat_history(session_id)
        return {"success": success, "message": "Chat history cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")