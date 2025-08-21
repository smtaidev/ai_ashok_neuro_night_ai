# app/core/AI_models.py
import os
from openai import AsyncOpenAI
from typing import List, Dict
from ..core.config import settings
from dotenv import load_dotenv


load_dotenv()

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

MODEL = "gpt-4o"
TEMPERATURE = 0.5
MAX_TOKENS = 1200

