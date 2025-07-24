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
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return json.dumps({"is_valid": False, "error_message": f"OpenAI API call failed: {e}"})

async def generate_gap_detection(request: GapDetectionRequest) -> Union[GapDetectionResponse, Dict]:
    validation_schema = {"type": "object", "properties": {
        "is_valid": {"type": "boolean"}, "error_message": {"type": "string", "description": "Reason for invalid input."},
        "analysis": GapDetectionResponse.model_json_schema()
    }}
    system_prompt = f"""You are a strategic AI advisor. First, validate if the user's input is business-relevant. If not, return a JSON object with "is_valid": false and an "error_message". If valid, return a JSON with "is_valid": true and the populated "analysis" object. Your response must conform to this schema: {json.dumps(validation_schema)}"""
    user_prompt = f"Context: {request.model_dump_json()}"
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
    system_prompt = f"""You are a strategic editor. First, validate the input themes. If not business-related, return JSON with "is_valid": false and an "error_message". If valid, return JSON with "is_valid": true and the "analysis" object populated with suggestions. Your response must conform to this schema: {json.dumps(validation_schema)}"""
    user_prompt = f"Improve the wording of these strategic themes: {request.model_dump_json()}"
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
    system_prompt = f"""You are a strategic planner. First, validate the input themes. If not business-related, return JSON with "is_valid": false and an "error_message". If valid, return JSON with "is_valid": true and the "analysis" object populated with mapped themes. Your response must conform to this schema: {json.dumps(validation_schema)}"""
    user_prompt = f"For each theme below, suggest 2-3 business goals: {request.model_dump_json()}"
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
    system_prompt = f"""You are an industry strategist. First, validate the company profile. If nonsensical, return JSON with "is_valid": false and an "error_message". If valid, return JSON with "is_valid": true and the "analysis" object populated with benchmark themes. Your response must conform to this schema: {json.dumps(validation_schema)}"""
    user_prompt = f"Based on this profile, suggest 3-4 common Strategic Themes for peers: {request.profile.model_dump()}"
    raw_response = await _call_openai_for_json(system_prompt, user_prompt)
    data = json.loads(raw_response)
    if not data.get("is_valid"):
        return {"error": data.get("error_message", "Company profile was deemed irrelevant.")}
    return BenchmarkingResponse(**data.get("analysis", {}))