# app/api/models/strategic_theme2_model.py
 
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
 
 # request validation: context information
class SWOTDataInput(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]
 
class ScoredChallengeInput(BaseModel):
    title: str
    category: str
    impact_on_business: str
    ability_to_address: str
    description: str
    risk_score: int
 
#  Input Models 
class ThemeItem(BaseModel):
    name: str
    description: str

class Competitor(BaseModel):
    name: str
    description: str

class Capability(BaseModel):
    capability: str
    type: Literal["Core", "Differentiating"]
 
class StrategyContext(BaseModel):
    vision: Optional[str] = None
    swot: Optional[SWOTDataInput] = None
    challenges: Optional[List[ScoredChallengeInput]] = None
    mission: Optional[str] = None
    value: Optional[str] = None
    purpose: Optional[str] = None
    customers: Optional[str] = None
    value_proposition: Optional[str] = None
    competitors: Optional[List[Competitor]] = None
    trends: Optional[str] = None
    capabilities: Optional[List[Capability]] = None

#  Main Request Model 
class CombinedAnalysisRequest(BaseModel):
    themes: List[ThemeItem]
    context: StrategyContext
    tone: Optional[str] = "coach"
 
#  Individual Request Models
class GapDetectionRequest(BaseModel):
    themes: List[ThemeItem]
    context: StrategyContext
 
class WordingSuggestionsRequest(BaseModel):
    themes: List[ThemeItem]
 
class GoalMappingRequest(BaseModel):
    themes: List[ThemeItem]
 
#  Response Models 
class GapDetectionResponse(BaseModel):
    missing_themes: str
    overlapping_themes: str
    unused_elements: str
 
class WordingSuggestion(BaseModel):
    original_name: str
    improved_name: str
    original_description: str
    improved_description: str
    rationale: str
 
class WordingSuggestionsResponse(BaseModel):
    suggestions: List[WordingSuggestion]
 
class MappedGoal(BaseModel):
    goal: str
    goal_type: str
 
class GoalMapping(BaseModel):
    theme_name: str
    goals: List[MappedGoal]
 
class GoalMappingResponse(BaseModel):
    mapped_themes: List[GoalMapping]

#  Final Combined Response Model
class CombinedResponse(BaseModel):
    gap_detection: Optional[GapDetectionResponse] = None
    wording_suggestions: Optional[WordingSuggestionsResponse] = None
    goal_mapping: Optional[GoalMappingResponse] = None
    error: Optional[str] = Field(None, description="An error message if the entire analysis process failed.")