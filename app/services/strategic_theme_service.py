from openai import AsyncOpenAI
from ..core.config import settings
from ..api.models.strategic_theme_model import StrategicThemeResponse
import re
import json

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

def _extract_json(text: str) -> dict:
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in strategic theme LLM response.")
    return json.loads(match.group(0))

async def process_strategic_theme(theme_text: str) -> StrategicThemeResponse:
    """
    Calls the OpenAI API to:
    1. Summarize the strategic theme
    2. Suggest improvements
    3. Provide 3 actionable initiatives related to the theme
    """

    system_prompt = """
    You are an expert in business strategy and organizational development. Given a strategic theme, your task is to analyze it and respond in structured JSON with the following keys:

    - theme_summary: a short summary of the theme in 1–2 sentences
    - theme_recommendations: list of 3 suggestions to clarify, expand, or sharpen the theme
    - strategic_initiatives: list of exactly 3 actionable initiatives that support the strategic theme

    Only return a valid JSON object. Do not include any explanations or extra text outside the JSON.
    """

    user_prompt = theme_text

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

    return StrategicThemeResponse(
        theme_summary=str(data.get("theme_summary", "")).strip(),
        theme_recommendations=data.get("theme_recommendations", [] if not isinstance(data.get("theme_recommendations"), list) else data.get("theme_recommendations")),
        strategic_initiatives=data.get("strategic_initiatives", [] if not isinstance(data.get("strategic_initiatives"), list) else data.get("strategic_initiatives"))
    )
