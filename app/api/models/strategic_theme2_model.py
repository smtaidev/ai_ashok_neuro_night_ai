from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from .swot_model import SWOTDataInput
from .challenge_model import ScoredChallengeInput

# --- Input Models ---
class ThemeItem(BaseModel):
    name: str
    description: str

class StrategyContext(BaseModel):
    vision: Optional[str] = None
    swot: Optional[SWOTDataInput] = None
    challenges: Optional[List[ScoredChallengeInput]] = None

class CompanyProfile(BaseModel):
    industry: Optional[str] = None
    size: Optional[str] = None
    region: Optional[str] = None
    businessModel: Optional[str] = None

class GapDetectionRequest(BaseModel):
    themes: List[ThemeItem]
    context: StrategyContext

class WordingSuggestionsRequest(BaseModel):
    themes: List[ThemeItem]

class GoalMappingRequest(BaseModel):
    themes: List[ThemeItem]

class BenchmarkingRequest(BaseModel):
    profile: CompanyProfile

# --- Response Models (Clean, Original Structure) ---
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

class BenchmarkTheme(BaseModel):
    theme_name: str
    description: str
    justification: str

class BenchmarkingResponse(BaseModel):
    benchmark_themes: List[BenchmarkTheme]