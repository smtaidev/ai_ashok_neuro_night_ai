# api/core/llm_client.py

# This module provides a client for interacting with the OpenAI API.

from openai import AsyncOpenAI
from config import settings

def get_llm_client():
    return AsyncOpenAI(api_key = settings.OPENAI_API_KEY)

