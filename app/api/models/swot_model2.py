# app/api/models/swot_analysis2_model.py

from pydantic import BaseModel, Field
from typing import List, Optional

# Import context models from other features

from .vision_model import VisionInput
from .trend_summary_model import TrendDataInput
from .challenge_model import ScoredChallengeInput

class SWOTDataInput(BaseModel):
    strengths: List[str] = []
    weaknesses: List[str] = []
    opportunities: List[str] = []
    threats: List[str] = []
# --- CONTEXT MODEL ---
# This model will hold all the optional contextual data from other AI features.

class SWOTContext(BaseModel):
    """Optional strategic context to provide a richer analysis."""
    vision: Optional[VisionInput] = None
    trends: Optional[TrendDataInput] = None
    challenges: Optional[List[ScoredChallengeInput]] = None

# --- REQUEST MODEL ---
# This is the main input model for the new endpoint.

class SWOTAnalysisRequestV2(BaseModel):
    swot: SWOTDataInput = Field(..., description="The core SWOT data (strengths, weaknesses, etc.).")
    context: Optional[SWOTContext] = Field(None, description="Optional strategic context from other analyses.")
    
    class Config:
        json_schema_extra = {
            "example": {
                "swot": {
                    "strengths": ["Strong regional dominance", "High customer satisfaction scores", "Recent sustainability awards"],
                    "weaknesses": ["Limited fleet electrification", "High driver turnover rate"],
                    "opportunities": ["State-level government incentives for green tech", "AI-driven route optimization potential"],
                    "threats": ["New national competitor entering market", "Rising fuel and maintenance costs"]
                },
                "context": {
                    "vision": {
                        "vision_statement": "To be the leading sustainable logistics provider in North America by 2030."
                    },
                    "challenges": [
                        {
                            "title": "Driver Retention",
                            "category": "HR",
                            "impact_on_business": "high",
                            "ability_to_address": "moderate",
                            "description": "Losing experienced drivers to competitors offering better benefits.",
                            "risk_score": 75
                        }
                    ]
                }
            }
        }

# --- RESPONSE MODELS ---
# These models define the new, detailed output format.

class SWOTScoreItem(BaseModel):
    value: float = Field(..., description="The calculated score for the category (1.0-10.0).")
    rationale: str = Field(..., description="A brief explanation for the score, linking to the SWOT data and context.")

class SWOTScoresWithRationale(BaseModel):
    strengths: SWOTScoreItem
    weaknesses: SWOTScoreItem
    opportunities: SWOTScoreItem
    threats: SWOTScoreItem

class SWOTRecommendationsV2(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]

class SWOTAnalysisResponseV2(BaseModel):
    scores: SWOTScoresWithRationale
    recommendations: SWOTRecommendationsV2
    error: Optional[str] = None