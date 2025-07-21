# app/services/strategic_theme2_service.py

from openai import AsyncOpenAI
import json # We'll need this to work with schemas
from ..core.config import settings
# We still import the parsers, but their job is much simpler now
from . import strategic_themes_parsers as parsers
from ..api.models.strategic_theme2_model import *

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def _call_openai_for_json(system_prompt: str, user_prompt: str) -> str:
    """A generic helper function to call the OpenAI API in JSON mode."""
    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            # This is the key to enforcing JSON output
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2 # Lower temperature for more predictable, structured output
        )
        return response.choices[0].message.content
    except Exception as e:
        # If the API call itself fails, return an error JSON
        return json.dumps({"error": f"OpenAI API call failed: {e}"})

# --- Service Functions for Each Endpoint (with new JSON-focused prompts) ---

async def generate_gap_detection(request: GapDetectionRequest) -> GapDetectionResponse:
    system_prompt = "You are a strategic AI advisor. Your response MUST be a single, valid JSON object that conforms to the provided schema. Do not include any explanatory text before or after the JSON."
    # We dynamically provide the Pydantic model's schema to the AI
    json_schema = GapDetectionResponse.model_json_schema()

    user_prompt = f"""
    Analyze the following company information to find gaps in their strategic themes.

    Company Vision: {request.context.vision}
    Company SWOT: {request.context.swot}
    Company Challenges: {request.context.challenges}
    Current Strategic Themes: {request.themes}
    
    Based on this, generate a JSON object with three keys: 'missing_themes', 'overlapping_themes', and 'unused_elements'.
    The JSON object must conform to this schema:
    {json.dumps(json_schema, indent=2)}
    """
    raw_response = await _call_openai_for_json(system_prompt, user_prompt)
    return parsers.json_to_gap_detection_response(raw_response)


async def generate_wording_suggestions(request: WordingSuggestionsRequest) -> WordingSuggestionsResponse:
    system_prompt = "You are a strategic editor. Your response MUST be a single, valid JSON object that conforms to the provided schema. Do not include any explanatory text."
    json_schema = WordingSuggestionsResponse.model_json_schema()
    
    user_prompt = f"""
    Improve the wording of these strategic themes: {request.themes}

    Generate a JSON object containing a single key "suggestions", which is a list of objects.
    Each object in the list must have five keys: 'original_name', 'improved_name', 'original_description', 'improved_description', and 'rationale'.
    The JSON object must conform to this schema:
    {json.dumps(json_schema, indent=2)}
    """
    raw_response = await _call_openai_for_json(system_prompt, user_prompt)
    return parsers.json_to_wording_suggestions_response(raw_response)


async def generate_goal_mapping(request: GoalMappingRequest) -> GoalMappingResponse:
    system_prompt = "You are a strategy AI. Your response MUST be a single, valid JSON object that conforms to the provided schema. Do not include any explanatory text."
    json_schema = GoalMappingResponse.model_json_schema()

    user_prompt = f"""
    For each strategic theme below, suggest 2-3 specific business goals.
    Themes: {request.themes}

    Generate a JSON object with a single key "mapped_themes", a list of objects.
    Each object should contain 'theme_name' and a 'goals' list. Each goal in the list should have a 'goal' and a 'goal_type'.
    The JSON object must conform to this schema:
    {json.dumps(json_schema, indent=2)}
    """
    raw_response = await _call_openai_for_json(system_prompt, user_prompt)
    return parsers.json_to_goal_mapping_response(raw_response)


async def generate_benchmarking(request: BenchmarkingRequest) -> BenchmarkingResponse:
    system_prompt = "You are an industry strategist. Your response MUST be a single, valid JSON object that conforms to the provided schema. Do not include any explanatory text."
    json_schema = BenchmarkingResponse.model_json_schema()

    user_prompt = f"""
    Based on this company profile, suggest 3-4 common Strategic Themes used by their peers.
    Profile: Industry '{request.profile.industry}', Size '{request.profile.size}', Business Model '{request.profile.model}'.

    Generate a JSON object with a single key "benchmark_themes", a list of objects.
    Each object must have three keys: 'theme_name', 'description', and 'justification'.
    The JSON object must conform to this schema:
    {json.dumps(json_schema, indent=2)}
    """
    raw_response = await _call_openai_for_json(system_prompt, user_prompt)
    return parsers.json_to_benchmarking_response(raw_response)