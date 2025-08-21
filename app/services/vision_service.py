from openai import AsyncOpenAI
import json
from typing import Union, Dict
from ..core.config import settings
from ..api.models.vision_model import VisionResponse, VisionInput

TONE_GUIDELINES = {
    "coach": "Your tone will be coach. Use a supportive, empathetic, and reassuring tone.",
    "advisor": "Your tone will be advisor. Use a sharp, executive-ready, and insight-focused tone.",
    "challenger": "Your tone will be challenger. Use a bold, urgent, and clarity-driven tone."
}
 
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def process_vision(request: VisionInput) -> Union[VisionResponse, Dict]:
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
    ✳️ Vision Statement Evaluation Prompt
 
    I’d like you to evaluate this vision statement both qualitatively and quantitatively.
    {TONE_GUIDELINES.get(request.tone, TONE_GUIDELINES["coach"])}

    Vision Statement:
    {request.vision_statement}

    Please provide:
    1. A score in percentage form (0–100%), broken down by the following criteria:
       – Clarity
       – Differentiation
       – Inspiration & Aspiration
       – Customer or Market Relevance
       – Timelessness
 
    2. An explanation for each category’s score and a brief summary of how the total was calculated.
 
    3. Recommendations on how to improve the vision statement—focusing on both content and emotional resonance.
 
    4. 3–5 alternative versions of the vision statement with different strategic tones, such as:
       – Customer-focused
       – Future-driven
       – Market-leading
       – Purpose-led
       – Innovation-driven
 
    The goal is to evolve the vision into something memorable, motivating, and future-proof—anchored in purpose and relevance.
 
    **CRITICAL INSTRUCTIONS:**
    1.  Invalid inputs include jokes, political statements, questions, or random nonsensical text.
    2.  If the input is INVALID, you MUST return a JSON object with "is_valid": false and an "error_message" explaining the issue.
    3.  If the input is VALID, you MUST return a JSON object with "is_valid": true and populate the "analysis" object with the evaluation.
 
    Your response MUST be ONLY a single, valid JSON object conforming to this schema:
    {json.dumps(validation_schema, indent=2)}
    """
 
    user_prompt = request.vision_statement
 
    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=1200  
        )
 
        content = response.choices[0].message.content.strip()
        data = json.loads(content)
 
        # Check the validation flag from the AI
        if not data.get("is_valid"):
            return {"error": data.get("error_message", "Input was deemed irrelevant for analysis.")}
       
        return VisionResponse(**data.get("analysis", {}))
 
    except Exception as e:
        return {"error": f"An unexpected error occurred during AI processing: {str(e)}"}