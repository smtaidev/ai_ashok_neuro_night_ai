from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional

# --- Input Model ---

class DifferentiationRequest(BaseModel):
    capability: str = Field(
        ..., 
        description="A short description of a skill or offering.",
        max_length=150
    )
    type: Literal["differentiating type"] = Field(
        ...,
        description="The type of analysis, must be 'differentiating type'."
    )

    # Custom validator to enforce the 10-word limit on 'capability'
    @field_validator('capability')
    def validate_word_count(cls, v: str) -> str:
        word_count = len(v.split())
        if word_count > 10:
            raise ValueError(f"Capability must be 10 words or fewer. You provided {word_count} words.")
        return v

# --- Output Model ---

class DifferentiationResponse(BaseModel):
    summary: str = Field(..., description="A 2-line AI-generated summary of the capability's unique value.")
    differentiating_factors: List[str] = Field(..., description="A list of 3 key points highlighting the differentiation.")
    error: Optional[str] = None