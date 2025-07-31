# app/api/models/business_goal2_model.py

from pydantic import BaseModel, Field
from typing import List, Optional, Literal

# --- Sub-Models for the Request ---

class ImpactRatings(BaseModel):
    risks: Literal["High", "Medium", "Low"]
    compliance: Literal["High", "Medium", "Low"]
    culture: Literal["High", "Medium", "Low"]
    change_management: Literal["High", "Medium", "Low"]
    l_and_d: Literal["High", "Medium", "Low"]
    capabilities: Literal["High", "Medium", "Low"]

class GoalItem(BaseModel):
    title: str
    description: str
    related_strategic_theme: str
    priority: Literal["High", "Medium", "Low"]
    resource_readiness: Literal["Yes", "No", "Partial"]
    assigned_functions: List[str]
    duration: Literal["Short-term", "Medium-term", "Long-term"]
    impact_ratings: ImpactRatings
    esg_issues: Literal["Yes", "No", "Uncertain"]
    new_capabilities_needed: Literal["Yes", "No"]
    existing_capabilities_to_enhance: Literal["Yes", "No"]

# --- Main Request Model ---

class BusinessGoalAnalysisRequest(BaseModel):
    vision: str
    strategic_themes: List[str]
    challenges: List[str]
    tone: Optional[Literal["coach", "advisor", "challenger"]] = "advisor"
    goals: List[GoalItem]

    class Config:
        json_schema_extra = {
            "example": {
                "vision": "To be the most innovative and sustainable tech solutions provider in emerging markets.",
                "strategic_themes": ["Digital Transformation", "Sustainable Growth", "Customer Centricity"],
                "challenges": ["Talent retention in tech roles", "Navigating international compliance", "Lack of unified onboarding process"],
                "tone": "advisor",
                "goals": [
                    {
                        "title": "Expand Cloud Services in Latin America",
                        "description": "Broaden our cloud service offerings across three new Latin American markets by end of year.",
                        "related_strategic_theme": "Digital Transformation",
                        "priority": "High",
                        "resource_readiness": "No",
                        "assigned_functions": ["Product", "Engineering", "Sales"],
                        "duration": "Long-term",
                        "impact_ratings": {
                            "risks": "High",
                            "compliance": "Medium",
                            "culture": "Low",
                            "change_management": "High",
                            "l_and_d": "Medium",
                            "capabilities": "High"
                        },
                        "esg_issues": "Yes",
                        "new_capabilities_needed": "Yes",
                        "existing_capabilities_to_enhance": "No"
                    },
                    {
                        "title": "Launch Unified Digital Onboarding",
                        "description": "Create a seamless digital onboarding experience for all new customers to reduce manual effort and improve initial satisfaction.",
                        "related_strategic_theme": "Customer Centricity",
                        "priority": "High",
                        "resource_readiness": "Partial",
                        "assigned_functions": ["Customer Success", "IT", "Product"],
                        "duration": "Medium-term",
                        "impact_ratings": {
                            "risks": "Low",
                            "compliance": "Low",
                            "culture": "Medium",
                            "change_management": "Medium",
                            "l_and_d": "Medium",
                            "capabilities": "No"
                        },
                        "esg_issues": "No",
                        "new_capabilities_needed": "No",
                        "existing_capabilities_to_enhance": "Yes"
                    }
                ]
            }
        }

# --- Sub-Models for the Response ---

class SMARTSuggestion(BaseModel):
    goal_title: str
    recommendation: str

class StrategicFitScore(BaseModel):
    goal_title: str
    score: float = Field(..., ge=0, le=100, description="Strategic fit score from 0 to 100.")
    comment: str

class DashboardInsights(BaseModel):
    risks: List[str]
    regulatory_compliances: List[str]
    roadblocks: List[str]
    talent: List[str]
    culture_realignment: List[str]
    change_management: List[str]
    learning_and_development: List[str]
    capabilities: List[str]

# --- Main Response Model ---

class BusinessGoalAnalysisResponse(BaseModel):
    alignment_summary: str
    smart_suggestions: List[SMARTSuggestion]
    strategic_priorities: List[str]
    strategic_fit_scores: List[StrategicFitScore]
    execution_watchouts: List[str]
    dashboard_insights: DashboardInsights
    error: Optional[str] = None