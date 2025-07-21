# app/services/vision_services.py


from openai import AsyncOpenAI
from ..core.config import settings
from ..api.models.vision_model import VisionResponse
import re
import json

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

def _extract_json(text: str) -> dict:
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in vision LLM response.")
    return json.loads(match.group(0))

async def process_vision(vision_text: str) -> VisionResponse:
    """
    Calls the OpenAI API to:
    1. Score the vision statement (1–100)
    2. Summarize it
    3. Suggest improvements
    4. Provide 3 improved alternative versions
    """

    system_prompt = """
    You are a seasoned business strategist. Analyze the following business vision statement and provide structured output as valid JSON only with these keys:

    - vision_score: integer (1–100) assessing clarity, ambition, and impact
    - vision_summary: concise summary (2-3 sentences) of strengths and weaknesses
    - vision_recommendations: list of actionable suggestions for improvement
    - vision_alternatives: list of exactly 3 rewritten vision statements that Concise & Bold plus Inspirational & Human-Centric Innovation-Focused & Strategic

    Return output EXACTLY as JSON, with no additional text.
    """

    user_prompt = vision_text

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=500
    )

    content = response.choices[0].message.content.strip()
    data = _extract_json(content)

    return VisionResponse(
        vision_score=int(data.get("vision_score", 0)),
        vision_summary=str(data.get("vision_summary", "")).strip(),
        vision_recommendations=data.get("vision_recommendations", [] if not isinstance(data.get("vision_recommendations"), list) else data.get("vision_recommendations")),
        vision_alt=data.get("vision_alternatives", [] if not isinstance(data.get("vision_alternatives"), list) else data.get("vision_alternatives"))
    )
