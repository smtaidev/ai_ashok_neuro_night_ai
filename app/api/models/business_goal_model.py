from pydantic import BaseModel, Field
from typing import List, Optional, Literal

# --- Reusable Sub-Models for Inputs (Unchanged) ---
class QuestionAnswerImpact(BaseModel):
    answer: Optional[str] = None
    impact: Optional[Literal["High", "Medium", "Low"]] = None

class NewCapabilityInfo(BaseModel):
    name: Optional[str] = None
    type: Optional[Literal["Core", "Differentiating", "Enabling"]] = None
    description: Optional[str] = None
    other_details: Optional[str] = None

class CapabilityInfo(BaseModel):
    influenced_capabilities: List[str] = Field(default_factory=list)
    owner: Optional[str] = None
    require_enhancing_capabilities: bool = False
    enhancement_details: Optional[str] = None
    require_new_capabilities: bool = False
    new_capability: Optional[NewCapabilityInfo] = None

# --- Main Request and Response Models ---
class BusinessGoalRequest(BaseModel):
    potential_risks_and_challenges: QuestionAnswerImpact
    regulatory_compliance: QuestionAnswerImpact
    cultural_realignment: QuestionAnswerImpact
    change_management: QuestionAnswerImpact
    learning_and_development: QuestionAnswerImpact
    capability_info: CapabilityInfo

# --- REVERTED Response Model (Clean Structure) ---
class BusinessGoalResponse(BaseModel):
    risks_summary: str
    regulatory_compliance_summary: str
    roadblocks_summary: str
    culture_realignment_summary: str
    change_management_summary: str
    learning_and_development_summary: str