from fastapi import APIRouter, Body, HTTPException
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
      },
      "capability_info": {
        "influenced_capabilities": ["Sales Process", "Customer Data Management"],
        "owner": "John Doe",
        "require_enhancing_capabilities": True,
        "enhancement_details": "We are upgrading our CRM to Salesforce Lightning to improve lead tracking.",
        "require_new_capabilities": False,
        "new_capability": None
      }
    })
):
    """
    Takes detailed information about a business goal and returns a structured
    AI-generated analysis of risks, compliance, and strategic realignments.
    """
    try:
        response = await business_goal_service.analyze_business_goal(request)
        if response.error:
            raise HTTPException(status_code=500, detail=response.error)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")