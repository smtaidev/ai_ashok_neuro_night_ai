# app/api/endpoints/vision.py

from fastapi import APIRouter, HTTPException, Body
from app.api.models.vision_model import VisionInput, VisionResponse
from app.services.vision_service import process_vision
router = APIRouter()

@router.post("/vision", response_model=VisionResponse, tags=["Vision"])

async def analyze_vision(input_data: VisionInput= Body(..., example={
    "vision_statement": "I want to create a sustainable business that lead in innovative technology solutions while prioritizing environmental responsibility and community engagement."
})
):
    """
    Analyze a business vision: scoring, summarizing, recommendations, alternatives.
    """
    try:
        return await process_vision(input_data.vision_statement)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vision processing failed: {str(e)}")
