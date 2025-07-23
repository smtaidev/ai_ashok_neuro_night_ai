import json
from pydantic import BaseModel, ValidationError
from app.api.models.business_goal_model import BusinessGoalResponse

def json_to_business_goal_response(text: str) -> BusinessGoalResponse:
    """
    Directly parses a JSON string into a BusinessGoalResponse model.
    If parsing fails, it returns an instance of the model with the error populated.
    """
    try:
        data = json.loads(text)
        return BusinessGoalResponse(**data)
    except (json.JSONDecodeError, ValidationError) as e:
        error_message = f"Failed to parse or validate AI response. Details: {e}. Raw Text: {text}"
        return BusinessGoalResponse(
            risks_summary="",
            regulatory_compliance_summary="",
            roadblocks_summary="",
            culture_realignment_summary="",
            change_management_summary="",
            learning_and_development_summary="",
            error=error_message
        )