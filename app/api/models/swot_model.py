# app/api/models/swot_model.py

from pydantic import BaseModel
from typing import List, Optional


class TokenUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    

# Request validation
class SWOTDataInput(BaseModel):
    strengths: List[str] = []
    weaknesses: List[str] = []
    opportunities: List[str] = []
    threats: List[str] = []


class SWOTScore(BaseModel):
    strengths_percentage: float
    weaknesses_percentage: float
    opportunities_percentage: float
    threats_percentage: float


class SWOTRecommendation(BaseModel):
    strengths_recommendation: str
    weaknesses_recommendation: str
    opportunities_recommendation: str
    threats_recommendation: str


# Base response validation
class SWOTAnalysisResponse(BaseModel):
    scores: SWOTScore
    recommendations: SWOTRecommendation
    token_usage: Optional[TokenUsage] = None


# Extended response including raw input/output and token usage metadata
class SWOTAnalysisWithMetaResponse(SWOTAnalysisResponse):
    input_text: str       # raw input prompt sent to AI
    output_text: str      # raw AI response text
