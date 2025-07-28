# app/api/endpoints/strategic_theme2.py
 
from fastapi import APIRouter, Body
from app.services import strategic_theme2_service as service
from app.api.models.strategic_theme2_model import CombinedAnalysisRequest, CombinedResponse
 
# This is the router object that main.py imports
router = APIRouter()
 
# Example for the documentation (profile key removed)
combined_analysis_example = {
  "themes": [
    {"name": "Digital Transformation", "description": "Modernize core infrastructure."},
    {"name": "Enhance Customer Experience", "description": "Improve support response times."}
  ],
  "context": {
    "vision": "To become the leading provider of sustainable packaging solutions.",
    "swot": {
        "strengths": ["Strong brand reputation"],
        "weaknesses": ["Limited international presence"],
        "opportunities": ["Growing market for eco-friendly products"],
        "threats": ["Rising raw material costs"]
    },
    "challenges": [
        {
            "title": "Supply Chain Volatility",
            "category": "Operations",
            "impact_on_business": "high",
            "ability_to_address": "moderate",
            "description": "Raw material prices are unpredictable.",
            "risk_score": 85
        }
    ],
    "mission": "Deliver sustainable packaging globally.",
    "value": "Eco-innovation, integrity, and transparency.",
    "purpose": "To reduce plastic waste through innovation.",
    "customers": "B2B companies seeking sustainable packaging.",
    "value_proposition": "Biodegradable solutions that protect the planet.",
    "competitors": ["EcoPack Inc", "GreenWrap Ltd"],
    "trends": ["Sustainability", "Bioplastics", "Circular economy"],
    "capabilities": ["Rapid prototyping", "Global distribution"]
  },
  "tone": "coach"
}
 
# The endpoint definition
@router.post("/combined-analysis", response_model=CombinedResponse, summary="Run a full strategic theme analysis")
async def analyze_combined(request: CombinedAnalysisRequest = Body(..., example=combined_analysis_example)):
    """
    This single endpoint performs a comprehensive analysis of strategic themes by combining:
    - **Gap Detection**: Identifies missing themes based on your business context.
    - **Wording Suggestions**: Improves the clarity and impact of your theme names and descriptions.
    - **Goal Mapping**: Connects your themes to concrete, actionable business goals.
   
    If any part of the analysis fails, a top-level error message will be returned.
    """
    if not request.themes:
        return CombinedResponse(error="At least one strategic theme is required for the analysis.")
       
    response = await service.generate_combined_analysis(request)
    return response