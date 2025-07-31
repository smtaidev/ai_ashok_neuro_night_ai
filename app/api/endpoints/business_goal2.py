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
        # The service function is designed to ALWAYS return a valid BusinessGoalAnalysisResponse object.
        # In case of validation failure, it populates the 'error' field itself.
        response = await business_goal_service2.analyze_business_goals(request)
        
        # --- THIS IS THE KEY CHANGE ---
        # We NO LONGER check for response.error and raise an exception here.
        # We simply return the response object as is. FastAPI will serialize it.
        # If there's an error, the JSON will have the error field populated and other fields
        # will be empty, exactly as you want. The status code will be 200 OK.
        return response

    except Exception as e:
        # This 'except' block is now only for TRUE unexpected server errors,
        # like the AI service being down or a critical bug in the code.
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected internal server error occurred: {str(e)}"
        )