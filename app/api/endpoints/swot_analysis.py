# app/api/endpoints/swot_analysis.py

from fastapi import APIRouter, Body, HTTPException
from app.api.models.swot_model import SWOTDataInput, SWOTAnalysisResponse
from app.services import swot_service

router = APIRouter()

@router.post(
    "/analysis",
    response_model=SWOTAnalysisResponse,
    summary="Generate SWOT Analysis with Scores and Recommendations",
    tags=["SWOT Analysis"]
)
async def create_swot_analysis(
    swot_data: SWOTDataInput = Body(..., example={
        "strengths": [
            "Strong brand recognition in the market",
            "Experienced management team with 15+ years in industry",
            "Robust financial position with healthy cash flow"
        ],
        "weaknesses": [
            "Limited digital presence compared to competitors",
            "High operational costs due to legacy systems"
        ],
        "opportunities": [
            "Emerging markets expansion potential in Asia",
            "New technology adoption could streamline operations",
            "Strategic partnerships with tech companies"
        ],
        "threats": [
            "Increasing competition from new market entrants",
            "Economic downturn affecting consumer spending",
            "Regulatory changes in key markets"
        ]
    })
):
    """
    Accepts SWOT data (lists of strings for Strengths, Weaknesses, Opportunities, Threats) and returns:
    1. AI-estimated percentage scores for each category based on strategic importance
    2. AI-generated recommendations for each category
    """
    try:
        analysis = await swot_service.generate_swot_analysis(swot_data)
        
        return analysis
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing SWOT analysis: {str(e)}"
        )
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))



