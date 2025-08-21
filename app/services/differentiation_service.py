from openai import AsyncOpenAI
import json
from typing import Union, Dict
from app.core.config import settings
from app.api.models.differentiation_model import DifferentiationRequest, DifferentiationResponse
 
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
 
async def _call_openai_for_json(system_prompt: str, user_prompt: str) -> str:
    """Helper function to call the OpenAI API in JSON mode."""
    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return json.dumps({"is_valid": False, "error_message": f"OpenAI API call failed: {e}"})
 
async def generate_differentiation_analysis(request: DifferentiationRequest) -> Union[DifferentiationResponse, Dict]:
    """
    Analyzes a user's capability. If irrelevant, returns an error dict.
    If valid, returns a DifferentiationResponse model.
    """
    validation_schema = {
        "type": "object",
        "properties": {
            "is_valid": {"type": "boolean"},
            "error_message": {"type": "string", "description": "Reason for invalid input, if applicable."},
            "analysis": DifferentiationResponse.model_json_schema()
        },
        "required": ["is_valid"]
    }
   
    system_prompt = f"""
    You are a brand and career strategist. First, validate if the user's input 'capability' is a plausible professional skill or offering.
 
    **CRITICAL INSTRUCTIONS:**
    1.  Invalid inputs include jokes, nonsensical text, questions, or anything clearly not a professional capability.
    2.  If the input is INVALID, you MUST return a JSON object with "is_valid": false and an "error_message" explaining why.
    3.  If the input is VALID, you MUST return a JSON object with "is_valid": true and populate the "analysis" object with a 'summary' and 3 'differentiating_factors'.
 
    Your response MUST be ONLY a single, valid JSON object conforming to this schema:
    """
   #    {json.dumps(validation_schema, indent=2)}
   
    user_prompt = f'Analyze this capability: "{request.capabilities}"'
   
    raw_response = await _call_openai_for_json(system_prompt, user_prompt)
    data = json.loads(raw_response)
 
    if not data.get("is_valid"):
        return {"error": data.get("error_message", "Input was deemed irrelevant for analysis.")}
   
    try:
        return DifferentiationResponse(**data.get("analysis", {}))
    except Exception as e:
        return {"error": f"Failed to parse the 'analysis' part of the AI response. Details: {e}"}