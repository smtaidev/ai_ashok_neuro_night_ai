from pydantic import BaseModel, Field, field_validator
from typing import List
 
# --- Input Model (Updated) ---
class DifferentiationRequest(BaseModel):
    """
    Input model that accepts a list of capabilities for differentiation analysis.
    """
    capabilities: List[str] = Field(
        ...,
        description="A list of skills or offerings to be analyzed (each max 10 words).",
        min_length=1
    )
 
    # @field_validator('capabilities')
    # def validate_each_capability_word_count(cls, v: List[str]) -> List[str]:
    #     """
    #     Validates each capability string in the list to ensure it is 10 words or fewer.
    #     """
    #     for capability_string in v:
    #         word_count = len(capability_string.split())
    #         if word_count > 10:
    #             raise ValueError(
    #                 f"Each capability must be 10 words or fewer. "
    #                 f"The following item exceeded the limit ({word_count} words): '{capability_string}'"
    #             )
    #     return v
 
# --- Output Model (Unchanged) ---
class DifferentiationResponse(BaseModel):
    """
    Response model containing the analysis of the provided capabilities.
    """
    summary: str = Field(..., description="A 2-line AI-generated summary of the combined unique value.")
    differentiating_factors: List[str] = Field(..., description="A list of 3 key points highlighting the overall differentiation.")