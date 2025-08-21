from fastapi import APIRouter, Body, HTTPException
from typing import Dict
from app.services import differentiation_service
from app.api.models.differentiation_model import DifferentiationRequest, DifferentiationResponse

router = APIRouter()

@router.post(
    "/analyze",
    response_model=DifferentiationResponse,
    summary="Generate Differentiation Analysis",
    tags=["Differentiation Analysis"]
)
async def analyze_differentiation(
    request: DifferentiationRequest = Body(..., example={
        "capabilities": [
            "I am a Python developer specializing in FastAPI.",
            "I create scalable web applications with a focus on performance.",
        ]
    })
):
    """
    Takes a user's capability and generates an analysis of its
    unique and differentiating factors. Rejects irrelevant input.
    """
    response = await differentiation_service.generate_differentiation_analysis(request)

    if isinstance(response, Dict) and "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])

    return response