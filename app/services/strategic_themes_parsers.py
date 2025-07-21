# app/services/strategic_theme2_parsers.py

import json
from pydantic import ValidationError
from ..api.models.strategic_theme2_model import *

# This single helper function can handle most parsing errors.
def _parse_json_to_model(text: str, model: BaseModel, error_response: BaseModel):
    try:
        data = json.loads(text)
        # Check for an error key from our own API call helper
        if "error" in data:
            # You can decide how to structure this error
            return error_response(error=data["error"])
        
        # Validate and instantiate the Pydantic model
        return model(**data)
    except (json.JSONDecodeError, ValidationError) as e:
        # The AI failed to produce valid JSON or it didn't match the schema
        return error_response(error=f"Failed to parse or validate AI response. Details: {e}. Raw Text: {text}")


# --- New, Simplified Parser Functions ---

def json_to_gap_detection_response(text: str) -> GapDetectionResponse:
    return _parse_json_to_model(
        text, 
        GapDetectionResponse, 
        # Provide a default error object
        GapDetectionResponse(missing_themes="error", overlapping_themes="error", unused_elements="error")
    )

def json_to_wording_suggestions_response(text: str) -> WordingSuggestionsResponse:
    return _parse_json_to_model(
        text, 
        WordingSuggestionsResponse, 
        WordingSuggestionsResponse(suggestions=[])
    )

def json_to_goal_mapping_response(text: str) -> GoalMappingResponse:
    return _parse_json_to_model(
        text, 
        GoalMappingResponse, 
        GoalMappingResponse(mapped_themes=[])
    )

def json_to_benchmarking_response(text: str) -> BenchmarkingResponse:
    return _parse_json_to_model(
        text, 
        BenchmarkingResponse, 
        BenchmarkingResponse(benchmark_themes=[])
    )