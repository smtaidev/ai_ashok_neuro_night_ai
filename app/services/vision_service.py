from openai import AsyncOpenAI
import json
from ..core.config import settings
from ..api.models.vision_model import VisionResponse, VisionInput

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def process_vision(vision_text: str) -> VisionResponse:
    """
    Analyzes the user's input.
    - If it's a valid business vision, it scores it and provides recommendations.
    - If it's irrelevant, it flags it as invalid and provides an error message.
    """
    # Get the JSON schema from our Pydantic model to guide the AI
    json_schema = VisionResponse.model_json_schema()

    # The new system prompt with negative prompting logic
    system_prompt = f"""
    You are a seasoned business strategist and an expert in evaluating corporate vision statements. Your primary task is to analyze the user's input and respond in a structured JSON format.

    **CRITICAL INSTRUCTIONS:**
    1.  **First, determine if the user's input is a plausible business vision statement.** A valid vision statement is a forward-looking declaration of a company's purpose and aspirations.
    2.  **Invalid inputs include:** simple questions (e.g., 'what is a vision?'), requests for jokes, political statements ('Trump is king'), personal opinions ('I love movies'), or random nonsensical text.
    3.  **If the input is INVALID:** You MUST return a JSON object where "is_valid" is false and "error_message" explains why the input is not a valid vision statement (e.g., "The provided text is a question, not a vision statement."). Do not populate the other fields.
    4.  **If the input is VALID:** You MUST return a JSON object where "is_valid" is true and you complete the following analysis:
        - "vision_score": An integer (1–100) assessing clarity, ambition, and impact.
        - "vision_summary": A concise 2-3 sentence summary of the vision's strengths and weaknesses.
        - "vision_recommendations": A list of actionable suggestions for improvement.
        - "vision_alt": A list of exactly 3 rewritten vision statements that are more Concise, Bold, and Strategic.

    **Your response MUST be ONLY a single, valid JSON object that conforms to this schema:**
    {json.dumps(json_schema, indent=2)}
    """

    user_prompt = vision_text

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"}, # Use reliable JSON mode
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=800
        )

        content = response.choices[0].message.content.strip()
        data = json.loads(content)

        # Directly instantiate the Pydantic model. It will validate the structure.
        return VisionResponse(**data)

    except Exception as e:
        # Handle cases where the API call itself or parsing fails
        return VisionResponse(
            is_valid=False,
            error_message=f"An unexpected error occurred during AI processing: {str(e)}"
        )