# backend/core.py
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4"  # or "gpt-4" if you prefer
    
    async def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": prompt}],  # Use system role for full context
                max_tokens=500,  # Increased for strategic responses
                temperature=0.5
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"