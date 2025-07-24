from fastapi import APIRouter, HTTPException, Body
from app.api.models.vision_model import VisionInput, VisionResponse
from app.services.vision_service import process_vision

router = APIRouter()

@router.post("/vision", response_model=VisionResponse, tags=["Vision"])
async def analyze_vision(
    input_data: VisionInput = Body(..., example={
        "vision_statement": "To create a sustainable business that leads in innovative technology solutions while prioritizing environmental responsibility and community engagement."
    })
):
    """
    Analyzes a business vision statement for its effectiveness and relevance.
    - If the input text is not a valid vision, it returns a 400 error.
    - If valid, it returns a score, summary, recommendations, and alternatives.
    """
    response = await process_vision(input_data.vision_statement)

    # If the AI flagged the input as invalid, return a 400 Bad Request error to the client.
    if not response.is_valid:
        raise HTTPException(
            status_code=400,
            detail=response.error_message or "The provided text was determined to be irrelevant or not a valid business vision statement."
        )

    # If the input was valid, return the full 200 OK response with the analysis.
    return response