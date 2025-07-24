from pydantic import BaseModel, Field
from typing import List

# Request validation
class VisionInput(BaseModel):
    """Input model for vision endpoint."""
    vision_statement: str

# Response validation (Reverted to original clean structure)
class VisionResponse(BaseModel):
    """
    Response model for a valid, processed vision analysis.
    """
    vision_score: int = Field(..., ge=0, le=100)
    vision_summary: str
    vision_recommendations: List[str]
    vision_alt: List[str] = Field(..., min_length=3, max_length=3)