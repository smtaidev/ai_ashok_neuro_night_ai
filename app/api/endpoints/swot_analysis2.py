# app/api/endpoints/swot_analysis2.py

from fastapi import APIRouter, Body, HTTPException
from ...api.models.swot_model2 import SWOTAnalysisRequestV2, SWOTAnalysisResponseV2
from ...services import swot_service2

router = APIRouter()

@router.post(
    "/analysis2",
    response_model=SWOTAnalysisResponseV2,
    summary="Generate Contextual SWOT Analysis",
    description="""
Generates a deep-dive SWOT analysis with scores (1-10) and actionable recommendations. 
This advanced version integrates optional strategic context, such as the company's vision, 
key challenges, strategic themes, and market trends, to produce a more nuanced and 
interconnected strategic assessment.
    """,
    tags=["SWOT Analysis"]
)
async def create_contextual_swot_analysis(
    request_data: SWOTAnalysisRequestV2 = Body(..., example=SWOTAnalysisRequestV2.Config.json_schema_extra["example"])
):
    """
    Accepts SWOT data and optional strategic context to return:
    1.  **Contextual Scores**: A score (1-10) and rationale for each SWOT category.
    2.  **Contextual Recommendations**: Actionable recommendations linked to the broader strategy.
    """
    try:
        analysis = await swot_service2.generate_contextual_swot_analysis(request_data)
        if analysis.error:
             raise HTTPException(
                status_code=500,
                detail=analysis.error
            )
        return analysis
    except Exception as e:
        # This catches exceptions from within the endpoint logic itself
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )