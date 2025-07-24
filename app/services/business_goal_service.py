from openai import AsyncOpenAI
import json
from typing import Union, Dict
from app.core.config import settings
from app.api.models.business_goal_model import BusinessGoalRequest, BusinessGoalResponse

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def _call_openai_for_json(system_prompt: str, user_prompt: str) -> str:
    """Helper function to call the OpenAI API in JSON mode."""
    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return json.dumps({"is_valid": False, "error_message": f"OpenAI API call failed: {e}"})

async def analyze_business_goal(request: BusinessGoalRequest) -> Union[BusinessGoalResponse, Dict]:
    """
    Analyzes user-provided answers for a business goal. If irrelevant, returns an error dict.
    If valid, returns a BusinessGoalResponse model.
    """
    # Define a schema that includes our validation fields
    validation_schema = {
        "type": "object",
        "properties": {
            "is_valid": {"type": "boolean"},
            "error_message": {"type": "string", "description": "Reason for invalid input, if applicable."},
            "analysis": BusinessGoalResponse.model_json_schema()
        },
        "required": ["is_valid"]
    }
    
    # Format the input data for the AI to easily see the answers
    input_data_text = f"""
    ### Goal Analysis Input Data
    1. Potential Risks Answer: "{request.potential_risks_and_challenges.answer or ""}"
    2. Regulatory Compliance Answer: "{request.regulatory_compliance.answer or ""}"
    3. Cultural Realignment Answer: "{request.cultural_realignment.answer or ""}"
    4. Change Management Answer: "{request.change_management.answer or ""}"
    5. Learning and Development Answer: "{request.learning_and_development.answer or ""}"
    (Capability information is provided for context only).
    """

    system_prompt = f"""
    You are a senior business strategist. Your first task is to validate the user's text `answer` fields for business relevance.

    **CRITICAL INSTRUCTIONS:**
    1.  Examine the five "Answer" fields provided in the user's input.
    2.  If **any** of the answers are clearly not business-related (e.g., jokes, nonsensical text, personal opinions, political statements), you MUST return a JSON object with "is_valid": false and an "error_message" specifying which answer was irrelevant and why.
    3.  If all the answers are business-relevant, you MUST return a JSON with "is_valid": true and populate the "analysis" object with six summaries based on ALL the provided context (including capabilities). For the "roadblocks_summary", synthesize information from risks, culture, and change management.

    Your response MUST be ONLY a single, valid JSON object conforming to this schema:
    {json.dumps(validation_schema, indent=2)}
    """
    
    # Send the full request data for context, but the prompt focuses validation on the answers
    user_prompt = f"Analyze this business goal data:\n{request.model_dump_json(indent=2)}"

    raw_response = await _call_openai_for_json(system_prompt, user_prompt)
    data = json.loads(raw_response)

    # Check the validation flag from the AI
    if not data.get("is_valid"):
        return {"error": data.get("error_message", "One or more answers were deemed irrelevant for analysis.")}

    # On success, return the validated Pydantic model from the nested 'analysis' key
    try:
        return BusinessGoalResponse(**data.get("analysis", {}))
    except Exception as e:
        return {"error": f"Failed to parse the 'analysis' part of the AI response. Details: {e}"}