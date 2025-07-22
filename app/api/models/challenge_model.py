# app/api/models/challenge_model.py

from pydantic import BaseModel
from typing import Literal
from app.api.models.trend_summary_model import TrendDataInput
from app.api.models.swot_model import SWOTDataInput
from typing import List

class ChallengeInput(BaseModel):
    title: str
    category: str
    impact_on_business: Literal["very low", "low", "moderate", "high", "very high"]
    ability_to_address: Literal["very low", "low", "moderate", "high", "very high"]
    description: str

class ScoredChallengeInput(ChallengeInput):
    risk_score: int

class ChallengeEvaluationRequest(BaseModel):
    challenge: ChallengeInput
    swot: SWOTDataInput
    trends: TrendDataInput

class ChallengeRiskScoreResponse(BaseModel):
    risk_score: int  # 1 to 100

class ChallengeRecommendationRequest(BaseModel):
    challenges: List[ScoredChallengeInput]  # 1 to 5 items
    swot: SWOTDataInput
    trends: TrendDataInput

class ChallengeRecommendationResponse(BaseModel):
    recommendations: str