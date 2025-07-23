from openai import AsyncOpenAI
import json
from app.core.config import settings
from app.utils import differentiation_parsers as parsers
from app.api.models.differentiation_model import DifferentiationRequest, DifferentiationResponse

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def _call_openai_for_json(system_prompt: str, user_prompt: str) -> str:
    """Helper function to call the OpenAI API in JSON mode."""
    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5 
        )
        return response.choices[0].message.content
    except Exception as e:
        return json.dumps({"error": f"OpenAI API call failed: {e}"})

#  The Main Service Function 

async def generate_differentiation_analysis(request: DifferentiationRequest) -> DifferentiationResponse:
    system_prompt = "You are a brand and career strategist. Your job is to take a user's self-described capability and articulate what makes it uniquely valuable and differentiating in a professional context. Your response must be a single, valid JSON object."
    json_schema = DifferentiationResponse.model_json_schema()
    
    user_prompt = f"""
    A user has described their capability as: "{request.capability}"

    Based on this, generate a JSON object that analyzes this capability. The object must contain exactly two keys:
    1.  'summary': A compelling, 2-line summary explaining the unique value of this capability.
    2.  'differentiating_factors': A JSON array containing exactly 3 distinct, concise bullet points that highlight what makes this capability stand out from others.

    The JSON object must conform to this schema:
    {json.dumps(json_schema, indent=2)}
    """

    raw_response = await _call_openai_for_json(system_prompt, user_prompt)
    return parsers.json_to_differentiation_response(raw_response)