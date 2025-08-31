# app/api/models/trend_summary_model.py

from pydantic import BaseModel
from typing import List, Optional
from ..models.strategic_theme2_model import Capability

# tracking token usages for AI 
class TokenUsage(BaseModel):
    input_tokens: int
    output_tokens: int
    total_tokens: int
    
    

# Validating the single question-answer-impact structure 
class TrendAnswer(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    impact: Optional[str] = None

# Validating the main INPUT model
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
    tone: Optional[str] = "coach"
    mission: Optional[str] = None
    value: Optional[str] = None
    purpose: Optional[str] = None
    capabilities: Optional[List[Capability]] = None
    



# This is the main OUTPUT model
class TrendSummaryResponse(BaseModel):
    key_opportunities: str
    strengths : str
    significant_risks: str
    challenges: str
    strategic_recommendations: str
    irrelevant_answers: List[str] = []  


# Validating the combined response model that includes both summary and top trends
class TrendCombinedResponse(BaseModel):
    summary: TrendSummaryResponse
    trend_synthesis: Optional[List[str]] = None
    early_warnings: Optional[str] = None
    strategic_opportunities: Optional[List[str]] = None
    analyst_recommendations: Optional[str] = None
    radar_executive_summary: Optional[List[str]] = []
    radar_recommendation: Optional[List[str]] = []
    error: Optional[str] = None
    token_count: Optional[TokenUsage] = None