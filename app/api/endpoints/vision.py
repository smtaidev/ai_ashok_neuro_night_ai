from fastapi import APIRouter, Body
from typing import Dict
from app.api.models.vision_model import VisionInput, VisionResponse
from app.services.vision_service import process_vision

router = APIRouter()

@router.post("/vision", response_model=VisionResponse, tags=["Vision"])
async def analyze_vision(
    input_data: VisionInput = Body(..., example={
        "vision_statement": "To create a sustainable business that leads in innovative technology solutions while prioritizing environmental responsibility and community engagement.",
        "tone": "coach"
    })
):
    """
    Analyzes a business vision statement for its effectiveness and relevance.
    Always returns 200 OK, including error details if any issue is found.
    """
    response = await process_vision(input_data)

    # Return either the successful response or the error as part of the 200 OK response
    if isinstance(response, Dict) and "error" in response:
        return VisionResponse(error=response["error"])

    return response