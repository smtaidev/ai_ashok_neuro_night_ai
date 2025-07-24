from pydantic import BaseModel, Field
from typing import List, Optional

class VisionInput(BaseModel):
    """Input model for vision endpoint."""
    vision_statement: str
    
class VisionResponse(BaseModel):
    """
    Response model for processed vision analysis.
    Now handles both valid and invalid input scenarios.
    """
    is_valid: bool = Field(..., description="True if the input was a valid vision, False otherwise.")
    error_message: Optional[str] = Field(None, description="Explains why the input was invalid, if applicable.")
    
    # These fields are now optional because they will be null for an invalid vision
    vision_score: Optional[int] = Field(None, ge=0, le=100)
    vision_summary: Optional[str] = None
    vision_recommendations: Optional[List[str]] = None
    vision_alt: Optional[List[str]] = Field(None, min_length=3, max_length=3)