# app/api/endpoints/business_goal2.py

from fastapi import APIRouter, Body, HTTPException
from ...services import business_goal_service2
from ...api.models.business_goal_model2 import BusinessGoalAnalysisRequest, BusinessGoalAnalysisResponse

router = APIRouter()

@router.post(
    "/analyze2",
    response_model=BusinessGoalAnalysisResponse,
    summary="Analyze Business Goal Portfolio",
    description="""
    Analyzes a portfolio of business goals against strategic context (vision, themes, challenges). 
    It returns a comprehensive strategic analysis including alignment summaries, SMART suggestions, 
    fit scores, priorities, and execution watchouts.
    
    If an input goal is determined to be irrelevant, the API will still return a 200 OK status, 
    but the response body will contain an error message in the 'error' field and other fields will be null or empty.
    """,
    tags=["Business Goals"]
)
async def analyze_goal_portfolio(
    request: BusinessGoalAnalysisRequest = Body(..., example=BusinessGoalAnalysisRequest.Config.json_schema_extra["example"])
):
    """
    Accepts a list of business goals and strategic context, then returns a detailed portfolio analysis.
    Handles business validation errors gracefully by returning a 200 OK response with an error message in the payload.
    """
    try:
        
        response = await business_goal_service2.analyze_business_goals(request)
        return response

    except Exception as e:
        
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected internal server error occurred: {str(e)}"
        )