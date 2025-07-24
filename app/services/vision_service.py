from openai import AsyncOpenAI
import json
from typing import Union, Dict
from ..core.config import settings
from ..api.models.vision_model import VisionResponse, VisionInput

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def process_vision(vision_text: str) -> Union[VisionResponse, Dict]:
    """
    Analyzes the user's input.
    - If it's a valid business vision, returns a VisionResponse Pydantic model.
    - If it's irrelevant, returns a dictionary with an 'error' key.
    """
    # Define a schema for the AI that includes our validation fields.
    # The AI will use this to structure its internal thinking.
    validation_schema = {
        "type": "object",
        "properties": {
            "is_valid": {"type": "boolean"},
            "error_message": {"type": "string", "description": "Reason for invalid input, if applicable."},
            "analysis": VisionResponse.model_json_schema()
        },
        "required": ["is_valid"]
    }
    
    system_prompt = f"""
    You are a seasoned business strategist. First, validate if the user's input is a plausible business vision statement.

    **CRITICAL INSTRUCTIONS:**
    1.  Invalid inputs include jokes, political statements, questions, or random nonsensical text.
    2.  If the input is INVALID, you MUST return a JSON object with "is_valid": false and an "error_message" explaining the issue.
    3.  If the input is VALID, you MUST return a JSON object with "is_valid": true and populate the "analysis" object with the 'vision_score', 'vision_summary', 'vision_recommendations', and 'vision_alt'.

    Your response MUST be ONLY a single, valid JSON object conforming to this schema:
    {json.dumps(validation_schema, indent=2)}
    """

    user_prompt = vision_text

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=800
        )

        content = response.choices[0].message.content.strip()
        data = json.loads(content)

        # Check the validation flag from the AI
        if not data.get("is_valid"):
            # Return the error dictionary
            return {"error": data.get("error_message", "Input was deemed irrelevant for analysis.")}
        
        # On success, return the Pydantic model from the nested 'analysis' key
        return VisionResponse(**data.get("analysis", {}))

    except Exception as e:
        # Handle cases where the API call itself or parsing fails
        return {"error": f"An unexpected error occurred during AI processing: {str(e)}"}