from pydantic import BaseModel, Field
from typing import List, Optional, Literal

# Reusable Sub-Models for Inputs 

class QuestionAnswerImpact(BaseModel):
    """Represents a question with a text answer and an impact rating."""
    answer: Optional[str] = None
    impact: Optional[Literal["High", "Medium", "Low"]] = None

class NewCapabilityInfo(BaseModel):
    """Represents the details of a new capability to be added."""
    name: Optional[str] = None
    type: Optional[Literal["Core", "Differentiating", "Enabling"]] = None
    description: Optional[str] = None
    other_details: Optional[str] = None

class CapabilityInfo(BaseModel):
    """Represents the capability-related section of the form."""
    influenced_capabilities: List[str] = Field(default_factory=list)
    owner: Optional[str] = None
    require_enhancing_capabilities: bool = False
    enhancement_details: Optional[str] = None
    require_new_capabilities: bool = False
    new_capability: Optional[NewCapabilityInfo] = None

# Main Request and Response Models

class BusinessGoalRequest(BaseModel):
    """The main input model for the entire business goal form."""
    # The five main text-based questions
    potential_risks_and_challenges: QuestionAnswerImpact
    regulatory_compliance: QuestionAnswerImpact
    cultural_realignment: QuestionAnswerImpact
    change_management: QuestionAnswerImpact
    learning_and_development: QuestionAnswerImpact
    # The nested capability information
    capability_info: CapabilityInfo

class BusinessGoalResponse(BaseModel):
    """The main output model for the AI-generated analysis."""
    risks_summary: str = Field(description="A bulleted list of top risks impacting the goal.")
    regulatory_compliance_summary: str = Field(description="A bulleted list of key compliance considerations.")
    roadblocks_summary: str = Field(description="A bulleted list of top roadblocks associated with the goal.")
    culture_realignment_summary: str = Field(description="A bulleted list of insights on cultural realignment.")
    change_management_summary: str = Field(description="A bulleted list of insights on change management.")
    learning_and_development_summary: str = Field(description="A bulleted list of insights on learning and development.")
    error: Optional[str] = None