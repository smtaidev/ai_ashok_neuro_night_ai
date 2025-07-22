# app/services/strategic_theme2_service.py

from openai import AsyncOpenAI
import json
from app.core.config import settings
from app.services import strategic_theme2_parsers as parsers # Using your renamed parser file
from app.api.models.strategic_theme2_model import * # Using your renamed model file

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

# --- The Single, Definitive Helper Function with Debugging ---
async def _call_openai_for_json(system_prompt: str, user_prompt: str) -> str:
    """Helper function to call the OpenAI API in JSON mode and print the response for debugging."""
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )
        raw_response_text = response.choices[0].message.content
        
        # This is the crucial debugging line
        print("--- AI Response Received ---")
        print(raw_response_text)
        print("--------------------------")

        return raw_response_text
        
    except Exception as e:
        # Also print the error if the API call itself fails
        print(f"!!! OpenAI API Call Failed: {e} !!!")
        return json.dumps({"error": f"OpenAI API call failed: {e}"})

# --- Service Functions (No changes needed here) ---

async def generate_gap_detection(request: GapDetectionRequest) -> GapDetectionResponse:
    system_prompt = "You are a strategic AI advisor. Your response MUST be a single, valid JSON object that conforms to the provided schema. Do not include any text outside the JSON object."
    json_schema = GapDetectionResponse.model_json_schema()
    user_prompt = f"""
    Analyze the company's Vision, SWOT, Challenges, and current Strategic Themes to identify gaps.
    Context:
    - Vision: {request.context.vision}
    - SWOT: {request.context.swot.model_dump_json(indent=2) if request.context.swot else 'Not provided'}
    - Challenges: {[c.model_dump() for c in request.context.challenges] if request.context.challenges else 'Not provided'}
    - Current Themes: {[t.model_dump() for t in request.themes]}
    
    Generate a JSON object with three keys: 'missing_themes', 'overlapping_themes', and 'unused_elements'.
    The JSON object must conform to this schema: {json.dumps(json_schema, indent=2)}
    """
    raw_response = await _call_openai_for_json(system_prompt, user_prompt)
    return parsers.json_to_gap_detection_response(raw_response)

async def generate_wording_suggestions(request: WordingSuggestionsRequest) -> WordingSuggestionsResponse:
    system_prompt = "You are a strategic editor. Your response MUST be a single, valid JSON object."
    json_schema = WordingSuggestionsResponse.model_json_schema()
    user_prompt = f"""
    Improve the wording of these strategic themes: {request.themes}
    Generate a JSON object containing a key "suggestions", a list of objects. Each object must have keys: 'original_name', 'improved_name', 'original_description', 'improved_description', 'rationale'.
    Conform to this schema: {json.dumps(json_schema, indent=2)}
    """
    raw_response = await _call_openai_for_json(system_prompt, user_prompt)
    return parsers.json_to_wording_suggestions_response(raw_response)

async def generate_goal_mapping(request: GoalMappingRequest) -> GoalMappingResponse:
    system_prompt = "You are a strategic planner. Your response MUST be a single, valid JSON object."
    json_schema = GoalMappingResponse.model_json_schema()
    user_prompt = f"""
    For each theme below, suggest 2-3 business goals.
    Themes: {request.themes}
    Generate a JSON with a key "mapped_themes", a list of objects. Each object has 'theme_name' and a 'goals' list. Each goal has a 'goal' and a 'goal_type' (Financial/Customer/Operational/Innovation/People).
    Conform to this schema: {json.dumps(json_schema, indent=2)}
    """
    raw_response = await _call_openai_for_json(system_prompt, user_prompt)
    return parsers.json_to_goal_mapping_response(raw_response)

async def generate_benchmarking(request: BenchmarkingRequest) -> BenchmarkingResponse:
    system_prompt = "You are an industry strategist. Your response MUST be a single, valid JSON object."
    json_schema = BenchmarkingResponse.model_json_schema()
    user_prompt = f"""
    Based on this profile, suggest 3-4 common Strategic Themes for peers.
    Profile: {request.profile.model_dump()}
    Generate a JSON object with a key "benchmark_themes", a list of objects. Each object must have 'theme_name', 'description', and 'justification'.
    Conform to this schema: {json.dumps(json_schema, indent=2)}
    """
    raw_response = await _call_openai_for_json(system_prompt, user_prompt)
    return parsers.json_to_benchmarking_response(raw_response)