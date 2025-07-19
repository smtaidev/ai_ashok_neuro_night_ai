# app/api/models/trend_summary_model.py

from pydantic import BaseModel
from typing import List, Optional

# Validating the single question-answer-impact structure 
class TrendAnswer(BaseModel):
    question: str
    answer: Optional[str] = None
    impact: Optional[str] = None  # Expected values: 'High', 'Medium', 'Low'

# Validating the main INPUT model. The JSON from the frontend must match this structure.
class TrendDataInput(BaseModel):
    customer_insights: List[TrendAnswer] = []
    competitor_landscape: List[TrendAnswer] = []
    technological_advances: List[TrendAnswer] = []
    regulatory_and_legal: List[TrendAnswer] = []
    economic_considerations: List[TrendAnswer] = []
    supply_chain_logistics: List[TrendAnswer] = []
    global_market_trends: List[TrendAnswer] = []
    environmental_social_impact: List[TrendAnswer] = []
    collaboration_partnerships: List[TrendAnswer] = []
    scenarios_risk_assessment: List[TrendAnswer] = []
    emerging_markets_opportunities: List[TrendAnswer] = []
    on_the_radar: List[TrendAnswer] = []

# This is the main OUTPUT model. Our API will guarantee the response matches this structure.
class TrendSummaryResponse(BaseModel):
    key_opportunities: str
    strengths : str
    significant_risks: str
    challenges: str
    strategic_recommendations: str
    irrelevant_answers: List[str] = []  # Add this line


# Validating the combined response model that includes both summary and top trends
class TrendCombinedResponse(BaseModel):
    summary: TrendSummaryResponse
    top_trends: List[str]
    radar_executive_summary: Optional[List[str]] = []
    radar_recommendation: Optional[List[str]] = []

