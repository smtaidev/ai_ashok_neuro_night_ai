# app/api/models/strategic_theme2_model.py

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


from .swot_model import SWOTDataInput
from .challenge_model import ScoredChallengeInput

# --- Shared Base Models ---

class ThemeItem(BaseModel):
    name: str
    description: str

class StrategyContext(BaseModel):
    """A container for all the contextual data needed for theme analysis."""
    vision: Optional[str] = None
    swot: Optional[SWOTDataInput] = None
    challenges: Optional[List[ScoredChallengeInput]] = None

class CompanyProfile(BaseModel):
    industry: Optional[str] = None
    size: Optional[str] = None # e.g., "10-50 employees"
    region: Optional[str] = None
    businessModel: Optional[str] = None

# --- Request Models for Each Endpoint ---

class GapDetectionRequest(BaseModel):
    themes: List[ThemeItem] = Field(..., description="List of current strategic themes.")
    context: StrategyContext

class WordingSuggestionsRequest(BaseModel):
    themes: List[ThemeItem] = Field(..., description="List of themes needing wording improvement.")

class GoalMappingRequest(BaseModel):
    themes: List[ThemeItem] = Field(..., description="List of themes to map goals to.")

class BenchmarkingRequest(BaseModel):
    profile: CompanyProfile

#  Response Models for Each Endpoint ---

class GapDetectionResponse(BaseModel):
    missing_themes: str
    overlapping_themes: str
    unused_elements: str
    error: Optional[str] = None

class WordingSuggestion(BaseModel):
    original_name: str
    improved_name: str
    original_description: str
    improved_description: str
    rationale: str

class WordingSuggestionsResponse(BaseModel):
    suggestions: List[WordingSuggestion]
    error: Optional[str] = None

class MappedGoal(BaseModel):
    goal: str
    goal_type: str

class GoalMapping(BaseModel):
    theme_name: str
    goals: List[MappedGoal]

class GoalMappingResponse(BaseModel):
    mapped_themes: List[GoalMapping]
    error: Optional[str] = None

class BenchmarkTheme(BaseModel):
    theme_name: str
    description: str
    justification: str

class BenchmarkingResponse(BaseModel):
    benchmark_themes: List[BenchmarkTheme]
    error: Optional[str] = None