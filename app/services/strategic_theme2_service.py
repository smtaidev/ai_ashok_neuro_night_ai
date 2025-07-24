from openai import AsyncOpenAI
import json
from typing import Union, Dict
from app.core.config import settings
from app.api.models.strategic_theme2_model import *

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def _call_openai_for_json(system_prompt: str, user_prompt: str) -> str:
    """Helper function to call the OpenAI API in JSON mode."""
    try:
        response = await client.chat.completions.create(
            model="gpt-4o", # Changed to gpt-4o for better instruction following
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return json.dumps({"is_valid": False, "error_message": f"OpenAI API call failed: {e}"})

# --- Service Functions with Clearer Dual-Task Prompts ---

async def generate_gap_detection(request: GapDetectionRequest) -> Union[GapDetectionResponse, Dict]:
    validation_schema = {"type": "object", "properties": {
        "is_valid": {"type": "boolean"}, "error_message": {"type": "string"},
        "analysis": GapDetectionResponse.model_json_schema()
    }}
    system_prompt = f"""
    You are a strategic AI advisor with two tasks.

    **Task 1: Validate Input.**
    First, examine the `description` of EACH theme in the user's 'Current Themes' list. If ANY description is nonsensical, a joke, or not a real business strategy, you MUST return a JSON with "is_valid": false and a specific "error_message".

    **Task 2: Perform Analysis (only if input is valid).**
    If ALL themes are valid, you MUST return a JSON with "is_valid": true. Then, you MUST populate the nested "analysis" object by thoroughly analyzing the full context (Vision, SWOT, Challenges) to generate insightful content for 'missing_themes', 'overlapping_themes', and 'unused_elements'. DO NOT return empty strings for the analysis.

    Your response must conform to this schema: {json.dumps(validation_schema)}
    """
    user_prompt = f"Please perform a gap analysis on the following business context: {request.model_dump_json(indent=2)}"
    raw_response = await _call_openai_for_json(system_prompt, user_prompt)
    data = json.loads(raw_response)

    if not data.get("is_valid"):
        return {"error": data.get("error_message", "Input was deemed irrelevant for analysis.")}
    return GapDetectionResponse(**data.get("analysis", {}))


async def generate_wording_suggestions(request: WordingSuggestionsRequest) -> Union[WordingSuggestionsResponse, Dict]:
    validation_schema = {"type": "object", "properties": {
        "is_valid": {"type": "boolean"}, "error_message": {"type": "string"},
        "analysis": WordingSuggestionsResponse.model_json_schema()
    }}
    system_prompt = f"""
    You are a strategic editor with two tasks.

    **Task 1: Validate Input.**
    First, examine the `description` of each theme. If any are nonsensical, you MUST return JSON with "is_valid": false and an "error_message".

    **Task 2: Perform Analysis (only if input is valid).**
    If all themes are valid, you MUST return JSON with "is_valid": true and populate the "analysis" object with detailed, improved wording suggestions. DO NOT return empty suggestions.
    
    Your response must conform to this schema: {json.dumps(validation_schema)}
    """
    user_prompt = f"Please provide wording suggestions for these themes: {request.model_dump_json(indent=2)}"
    raw_response = await _call_openai_for_json(system_prompt, user_prompt)
    data = json.loads(raw_response)

    if not data.get("is_valid"):
        return {"error": data.get("error_message", "Input themes were deemed irrelevant.")}
    return WordingSuggestionsResponse(**data.get("analysis", {}))


async def generate_goal_mapping(request: GoalMappingRequest) -> Union[GoalMappingResponse, Dict]:
    validation_schema = {"type": "object", "properties": {
        "is_valid": {"type": "boolean"}, "error_message": {"type": "string"},
        "analysis": GoalMappingResponse.model_json_schema()
    }}
    system_prompt = f"""
    You are a strategic planner with two tasks.

    **Task 1: Validate Input.**
    First, examine the `description` of each theme. If any are nonsensical, you MUST return JSON with "is_valid": false and an "error_message".

    **Task 2: Perform Analysis (only if input is valid).**
    If all themes are valid, you MUST return JSON with "is_valid": true and populate the "analysis" object by mapping 2-3 specific business goals to each theme. DO NOT return an empty list of goals.
    
    Your response must conform to this schema: {json.dumps(validation_schema)}
    """
    user_prompt = f"Please map business goals to the following themes: {request.model_dump_json(indent=2)}"
    raw_response = await _call_openai_for_json(system_prompt, user_prompt)
    data = json.loads(raw_response)

    if not data.get("is_valid"):
        return {"error": data.get("error_message", "Input themes were deemed irrelevant.")}
    return GoalMappingResponse(**data.get("analysis", {}))


async def generate_benchmarking(request: BenchmarkingRequest) -> Union[BenchmarkingResponse, Dict]:
    validation_schema = {"type": "object", "properties": {
        "is_valid": {"type": "boolean"}, "error_message": {"type": "string"},
        "analysis": BenchmarkingResponse.model_json_schema()
    }}
    system_prompt = f"""
    You are an industry strategist with two tasks.

    **Task 1: Validate Input.**
    First, examine the company profile. If any part is nonsensical (e.g., industry: 'making jokes'), you MUST return JSON with "is_valid": false and an "error_message".

    **Task 2: Perform Analysis (only if input is valid).**
    If the profile is valid, you MUST return JSON with "is_valid": true and populate the "analysis" object with 3-4 common strategic themes for peers. DO NOT return an empty list.

    Your response must conform to this schema: {json.dumps(validation_schema)}
    """
    user_prompt = f"Please provide benchmark themes for this company profile: {request.profile.model_dump()}"
    raw_response = await _call_openai_for_json(system_prompt, user_prompt)
    data = json.loads(raw_response)

    if not data.get("is_valid"):
        return {"error": data.get("error_message", "Company profile was deemed irrelevant.")}
    return BenchmarkingResponse(**data.get("analysis", {}))