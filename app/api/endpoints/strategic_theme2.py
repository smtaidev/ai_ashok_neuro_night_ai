# app/api/endpoints/strategic_theme2.py
 
from fastapi import APIRouter, Body
from app.services import strategic_theme2_service as service
from app.api.models.strategic_theme2_model import CombinedAnalysisRequest, CombinedResponse
 
router = APIRouter()
 
combined_analysis_example = {
  "themes": [
    {
      "name": "Digital Transformation",
      "description": "Modernize internal systems and customer-facing platforms to improve agility and user experience."
    },
    {
      "name": "Customer Centricity",
      "description": "Enhance customer relationships by personalizing services and streamlining engagement processes."
    }
  ],
  "context": {
    "vision": "To be the leading provider of agile and sustainable digital solutions in emerging markets.",
    "swot": {
      "strengths": [
        "Strong brand presence in Southeast Asia",
        "Robust engineering talent"
      ],
      "weaknesses": [
        "Slow decision-making process",
        "Limited automation in customer service"
      ],
      "opportunities": [
        "Growing demand for digital transformation",
        "Government support for tech innovation"
      ],
      "threats": [
        "New market entrants with disruptive pricing",
        "Changing data privacy regulations"
      ]
    },
    "challenges": [
      {
        "title": "Improve Talent Retention",
        "category": "HR",
        "impact_on_business": "High",
        "ability_to_address": "Medium",
        "description": "Attrition in key engineering roles has increased over the past year.",
        "risk_score": 8
      },
      {
        "title": "Ensure GDPR Compliance",
        "category": "Regulatory",
        "impact_on_business": "High",
        "ability_to_address": "High",
        "description": "New products must comply with GDPR to avoid penalties.",
        "risk_score": 9
      }
    ],
    "mission": "Deliver digital innovation with integrity and speed.",
    "value": "Customer obsession and operational excellence.",
    "purpose": "Empower businesses with transformative digital tools.",
    "customers": "Enterprises in fintech, healthcare, and e-commerce sectors.",
    "value_proposition": "We simplify complex digital transformation for growth-stage companies.",
    "competitors": [
      {
        "name": "NextGen Tech",
        "description": "A fast-scaling competitor offering AI-based workflow tools."
      },
      {
        "name": "Agilisys",
        "description": "Focused on public-sector digital transformation with strong data compliance posture."
      }
    ],
    "trends": "AI integration, Hyper-personalization, Remote workforce enablement",
    "capabilities": [
      {
        "capability": "Data Analytics",
        "type": "Core"
      },
      {
        "capability": "AI Automation",
        "type": "Differentiating"
      },
      {
        "capability": "Customer Relationship Management",
        "type": "Differentiating"
      }
    ]
  },
  "tone": "advisor"
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