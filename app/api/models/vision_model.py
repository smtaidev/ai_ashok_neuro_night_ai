from pydantic import BaseModel, Field
from typing import List, Optional

# Request validation
class VisionInput(BaseModel):
    """Input model for vision endpoint."""
    vision_statement: str
    tone: Optional[str] = "coach"

# Response validation 
class VisionResponse(BaseModel):
    """
    Response model for a valid or invalid vision analysis.
    """
    vision_score: Optional[int] = Field(None, ge=0, le=100)
    vision_summary: Optional[str] = None
    vision_recommendations: Optional[List[str]] = None
    vision_alt: Optional[List[str]] = Field(default=None, min_length=3, max_length=3)
    error: Optional[str] = None 