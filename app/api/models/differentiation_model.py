from pydantic import BaseModel, Field, field_validator
from typing import List

# --- Input Model (Simplified) ---
class DifferentiationRequest(BaseModel):
    capability: str = Field(
        ...,
        description="A short description of a skill or offering (max 10 words).",
        max_length=150
    )

    # The word-count validator remains, as it's still relevant.
    @field_validator('capability')
    def validate_word_count(cls, v: str) -> str:
        word_count = len(v.split())
        if word_count > 10:
            raise ValueError(f"Capability must be 10 words or fewer. You provided {word_count} words.")
        return v

# --- Output Model (Unchanged) ---
class DifferentiationResponse(BaseModel):
    summary: str = Field(..., description="A 2-line AI-generated summary of the capability's unique value.")
    differentiating_factors: List[str] = Field(..., description="A list of 3 key points highlighting the differentiation.")