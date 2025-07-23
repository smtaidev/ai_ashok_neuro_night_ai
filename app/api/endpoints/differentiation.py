from fastapi import APIRouter, Body, HTTPException
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
        "capability": "I am a Python developer specializing in FastAPI.",
        "type": "differentiating type"
    })
):
    """
    Takes a user's capability and generates an analysis of its
    unique and differentiating factors.
    """
    try:
        response = await differentiation_service.generate_differentiation_analysis(request)
        if response.error:
            # Propagate errors from the service layer as a 500 error
            raise HTTPException(status_code=500, detail=response.error)
        return response
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")