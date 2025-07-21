# app/api/models/strategic_theme2_model.py

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# --- Shared Base Models ---

class ThemeItem(BaseModel):
    name: str
    description: str

class StrategyContext(BaseModel):
    vision: Optional[str] = None
    capabilities: Optional[str] = None
    swot: Optional[Dict[str, Any]] = None # Can be a complex object
    challenges: Optional[List[str]] = None

class CompanyProfile(BaseModel):
    industry: Optional[str] = None
    size: Optional[str] = None # e.g., "10-50 employees", "1000+ employees"
    region: Optional[str] = None
    model: Optional[str] = Field(None, alias="businessModel") # e.g., "B2B SaaS", "D2C E-commerce"

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




# --- Response Models for Each Endpoint ---

# A. Gap Detection
class GapDetectionResponse(BaseModel):
    missing_themes: str
    overlapping_themes: str
    unused_elements: str

# B. Wording Suggestions
class WordingSuggestion(BaseModel):
    original_name: str
    improved_name: str
    original_description: str
    improved_description: str
    rationale: str

class WordingSuggestionsResponse(BaseModel):
    suggestions: List[WordingSuggestion]

# C. Goal Mapping
class MappedGoal(BaseModel):
    goal: str
    goal_type: str

class GoalMapping(BaseModel):
    theme_name: str
    goals: List[MappedGoal]

class GoalMappingResponse(BaseModel):
    mapped_themes: List[GoalMapping]

# D. Benchmarking
class BenchmarkTheme(BaseModel):
    theme_name: str
    description: str
    justification: str

class BenchmarkingResponse(BaseModel):
    benchmark_themes: List[BenchmarkTheme]