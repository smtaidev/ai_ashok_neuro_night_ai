import json
from pydantic import BaseModel, ValidationError
from app.api.models.differentiation_model import DifferentiationResponse

def json_to_differentiation_response(text: str) -> DifferentiationResponse:
    """
    Directly parses a JSON string into a DifferentiationResponse model.
    If parsing fails, it returns an instance of the model with the error populated.
    """
    try:
        data = json.loads(text)
        return DifferentiationResponse(**data)
    except (json.JSONDecodeError, ValidationError) as e:
        error_message = f"Failed to parse or validate AI response. Details: {e}. Raw Text: {text}"
        return DifferentiationResponse(
            summary="",
            differentiating_factors=[],
            error=error_message
        )