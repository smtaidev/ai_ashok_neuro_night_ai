from fastapi import APIRouter, HTTPException, Body
from typing import Dict
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
    # The service returns either the model or an error dict
    response = await process_vision(input_data.vision_statement)

    # Check the type of the response to determine the outcome
    if isinstance(response, Dict) and "error" in response:
        # If it's a dict with an error, raise a 400 Bad Request
        raise HTTPException(
            status_code=400,
            detail=response["error"]
        )

    # If we get here, the response is a valid VisionResponse model.
    # FastAPI automatically sends it with a 200 OK status.
    return response