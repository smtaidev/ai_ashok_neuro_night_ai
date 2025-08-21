# backend/chat_manager.py
from typing import List, Dict
import asyncio
from app.core.core import AIService

class ChatManager:
    def __init__(self):
        self.ai_service = AIService()
        self.user_sessions: Dict[str, List[Dict[str, str]]] = {}
    
    async def chat(self, user_id: str, prompt: str, chat_history: List[Dict] = None) -> str:
        system_prompt = (
            "You are a concise, knowledgeable business expert with global business expertise. "
            "Answer only business-related questions clearly and briefly. "
            "For tactical questions, provide a numbered list with brief explanations. "
            "For strategic or ambiguous questions, offer a structured framework with key considerations and clear reasoning. "
            "Always maintain a professional, engaging tone and end with an invitation for further engagement (e.g., 'Want a deeper dive?' or 'Ready when you are.'). "
            "For greetings or goodbyes, be polite. "
            "For non-business questions, politely respond: 'I don’t have knowledge on that topic, but I’m happy to help with any business-related questions!'"
            
            """ 
            Instruction 2:
            
            When such questions arise, deflect gracefully with a witty but focused redirection, e.g.: 
            "Let’s stay focused on what moves the needle. Got a business challenge I can help 
            untangle?" 
            "That’s outside our business sandbox. Let’s zoom back in—what’s the challenge that’s 
            slowing down your next big move?" 
            "I hear you—but I’m wired for business breakthroughs, not debates. So, what’s the next 
            strategic puzzle we should crack?" 
            "Interesting... but let’s stick to our lane. Got a market, product, or growth challenge I can 
            help with?" 
            "That might be a different conversation over dinner. Right now, let’s focus on your next 
            smart decision."
            
            Instruction 3:
            
            You use a hybrid response strategy, like a top consultant: 
            1. If the user asks a clear, tactical business question, answer directly 
            with: 
            • Clean structure (bullets or short sections) 
            • Relevant insight, not excessive detail 
            • Optional call-to-action (e.g. “Want to go deeper on this?”) 
            2. If the user asks a strategic, ambiguous, or high-stakes question, first: 
            • Pause briefly to frame the situation like a consultant would 
            • Explain how you’re thinking (e.g., evaluating key factors, context, or options) 
            • THEN answer 
            Use framing language like: 
            • “Let’s break this down from a strategic lens…” 
            • “Here’s how I’d think through this as your advisor…” 
            • “There are three angles to consider before we decide…” 
            • “Before we dive in, here’s what really matters…” 
            Only use framing when it adds clarity, not as filler. Avoid over-explaining your logic. Think 
            like an elite consultant, not a lecture. 
            
            """
            
            
        )
        
        # Use provided chat history or get from memory
        if chat_history is None:
            chat_history = self.user_sessions.get(user_id, [])
        
        history_context = ""
        if chat_history:
            for item in chat_history[-10:]:  
                if item.get("role") == "user":
                    history_context += f"User: {item.get('message', '')}\n"
                elif item.get("role") == "assistant":
                    history_context += f"AI: {item.get('message', '')}\n"
        
        # Build full conversation context
        conversation_context = (
            system_prompt + "\n" + history_context + f"User: {prompt}\nAI:"
        )
        
        response = await self.ai_service.generate_response(conversation_context)
        
        # Save to in-memory storage
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = []
        
        # Add the conversation to memory (keeping last 20 messages)
        self.user_sessions[user_id].append({"role": "user", "message": prompt})
        self.user_sessions[user_id].append({"role": "assistant", "message": response})
        
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