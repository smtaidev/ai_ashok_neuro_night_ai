# backend/chat_manager.py
from typing import List, Dict
import asyncio
from app.core.core import AIService

class ChatManager:
    def __init__(self):
        self.ai_service = AIService()
        # In-memory storage for chat sessions (will be lost on restart)
        self.user_sessions: Dict[str, List[Dict[str, str]]] = {}
    
    async def chat(self, user_id: str, prompt: str, chat_history: List[Dict] = None) -> str:
        system_prompt = (
            "You are a super concise knowledgeable business expert. "
            "You have all the knowledge of the world about businesses. "
            "You strictly answer only business-related questions, clearly and briefly. "
            "If you see someone asks you outside of business, you simply say you don't have knowledge on that.\n"
        )
        
        # Use provided chat history or get from memory
        if chat_history is None:
            chat_history = self.user_sessions.get(user_id, [])
        
        # Build conversation context from history
        history_context = ""
        if chat_history:
            for item in chat_history[-10:]:  # Keep last 10 messages for context
                if item.get("role") == "user":
                    history_context += f"User: {item.get('message', '')}\n"
                elif item.get("role") == "assistant":
                    history_context += f"AI: {item.get('message', '')}\n"
        
        # Build full conversation context
        conversation_context = (
            system_prompt + "\n" + history_context + f"User: {prompt}\nAI:"
        )
        
        # Call AI to generate response
        response = await self.ai_service.generate_response(conversation_context)
        
        # Save to in-memory storage
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = []
        
        # Add the conversation to memory (keeping last 20 messages)
        self.user_sessions[user_id].append({"role": "user", "message": prompt})
        self.user_sessions[user_id].append({"role": "assistant", "message": response})
        
        # Keep only last 20 messages to prevent memory overflow
        if len(self.user_sessions[user_id]) > 20:
            self.user_sessions[user_id] = self.user_sessions[user_id][-20:]
        
        return response
    
    def get_chat_history(self, user_id: str) -> List[Dict]:
        """Get chat history for a user"""
        return self.user_sessions.get(user_id, [])
    
    def clear_chat_history(self, user_id: str) -> bool:
        """Clear chat history for a user"""
        if user_id in self.user_sessions:
            self.user_sessions[user_id] = []
            return True
        return False