from pydantic import BaseModel, Field, field_validator
from typing import List
 
#  Input Model 
class DifferentiationRequest(BaseModel):
    """
    Input model that accepts a list of capabilities for differentiation analysis.
    """
    capabilities: List[str] = Field(
        ...,
        description="A list of skills or offerings to be analyzed (each max 10 words).",
        min_length=1
    )
 
# Output Model
class DifferentiationResponse(BaseModel):
    """
    Response model containing the analysis of the provided capabilities.
    """
    summary: str = Field(..., description="A 2-line AI-generated summary of the combined unique value.")
    differentiating_factors: List[str] = Field(..., description="A list of 3 key points highlighting the overall differentiation.")