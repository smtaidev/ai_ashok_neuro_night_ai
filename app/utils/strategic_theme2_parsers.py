# import json
# from pydantic import BaseModel, ValidationError
# from app.api.models.strategic_theme2_model import *

# def _parse_json_to_model(text: str, model_class: type[BaseModel]):
#     """
#     Directly parses a JSON string into a Pydantic model.
#     If parsing fails, it returns an instance of the same model with the error populated.
#     """
#     try:
#         data = json.loads(text)
#         return model_class(**data)
#     except (json.JSONDecodeError, ValidationError) as e:
#         error_message = f"Failed to parse or validate AI response. Details: {e}. Raw Text: {text}"
        
#         default_data = {}
#         for field_name, field_info in model_class.model_fields.items():
#             if field_info.is_required():
#                 default_data[field_name] = [] if "List" in str(field_info.annotation) else ""
        
#         default_data['error'] = error_message
#         return model_class(**default_data)


# def json_to_gap_detection_response(text: str) -> GapDetectionResponse:
#     return _parse_json_to_model(text, GapDetectionResponse)

# def json_to_wording_suggestions_response(text: str) -> WordingSuggestionsResponse:
#     return _parse_json_to_model(text, WordingSuggestionsResponse)

# def json_to_goal_mapping_response(text: str) -> GoalMappingResponse:
#     return _parse_json_to_model(text, GoalMappingResponse)

# # def json_to_benchmarking_response(text: str) -> BenchmarkingResponse:
# #     return _parse_json_to_model(text, BenchmarkingResponse)