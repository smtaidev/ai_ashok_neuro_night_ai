from fastapi import APIRouter, Body, HTTPException
from typing import Dict
from app.services import business_goal_service
from app.api.models.business_goal_model import BusinessGoalRequest, BusinessGoalResponse
 
router = APIRouter()
 
@router.post(
    "/analyze",
    response_model=BusinessGoalResponse,
    summary="Generate Business Goal Analysis",
    tags=["Business Goals"]
)
async def create_business_goal_analysis(
    request: BusinessGoalRequest = Body(..., example={
      "potential_risks_and_challenges": {
        "answer": "Market competition is intensifying, and there's a risk of technological disruption from new entrants.",
        "impact": "High"
      },
      "regulatory_compliance": {
        "answer": "We need to ensure compliance with new data privacy laws like GDPR and CCPA.",
        "impact": "High"
      },
      "cultural_realignment": {
        "answer": "A shift towards a more data-driven and agile culture is necessary. This requires training and a change in mindset.",
        "impact": "Medium"
      },
      "change_management": {
        "answer": "We need a clear communication plan and stakeholder buy-in to manage the transition to our new CRM system.",
        "impact": "Medium"
      },
      "learning_and_development": {
        "answer": "The sales team needs training on the new CRM and advanced data analysis techniques.",
        "impact": "Low"
      }
    })
):
    """
    Takes detailed information about a business goal and returns a structured
    AI-generated analysis. Rejects irrelevant answers.
    """
    # The service returns either the model or an error dict
    response = await business_goal_service.analyze_business_goal(request)
 
    # Check the type of the response to determine the outcome
    if isinstance(response, Dict) and "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
 
    # If we get here, the response is a valid BusinessGoalResponse model
    return response