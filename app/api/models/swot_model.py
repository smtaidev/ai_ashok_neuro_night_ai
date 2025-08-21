# app/api/models/swot_model.py

from pydantic import BaseModel
from typing import List

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

# Response validation
class SWOTAnalysisResponse(BaseModel):
    scores: SWOTScore
    recommendations: SWOTRecommendation