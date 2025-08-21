# app/services/strategic_theme2_service.py

from openai import AsyncOpenAI
import json
import asyncio
from app.core.config import settings
from app.api.models.strategic_theme2_model import *
from fastapi import HTTPException

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

TONE_GUIDELINES = {
    "coach": "Your tone will be coach. Use a supportive, empathetic, and reassuring tone.",
    "advisor": "Your tone will be advisor. Use a sharp, executive-ready, and insight-focused tone.",
    "challenger": "Your tone will be challenger. Use a bold, urgent, and clarity-driven tone."
}

INSTRUCTIONS = """
Instructions: 
1. If multiple inputs are missing, begin with a supportive 
recommendation to complete them before moving forward. 
2. If enough inputs are available, provide constructive feedback on 
the strategic themes or suggest key themes the user might explore. 
3. Use emotionally resonant, leadership-ready language. Avoid 
referencing confidential details or asking for additional sensitive 
input. 
4. Keep the tone aligned with the selected style (coach, advisor, 
challenger).
"""

async def generate_combined_analysis(request: CombinedAnalysisRequest) -> CombinedResponse:
    """
    Orchestrates the analyses. If any fails, it catches the exception
    and returns a response with a top-level error message.
    """
    try:
        tone = request.tone or "coach"
        tone_guideline = TONE_GUIDELINES.get(tone, TONE_GUIDELINES["coach"])

        gap_request = GapDetectionRequest(themes=request.themes, context=request.context)
        wording_request = WordingSuggestionsRequest(themes=request.themes)
        goal_request = GoalMappingRequest(themes=request.themes)

        gap_result, wording_result, goal_result = await asyncio.gather(
            generate_gap_detection(gap_request, tone_guideline),
            generate_wording_suggestions(wording_request, tone_guideline),
            generate_goal_mapping(goal_request, tone_guideline)
        )

        return CombinedResponse(
            gap_detection=gap_result,
            wording_suggestions=wording_result,
            goal_mapping=goal_result
        )
    except HTTPException as e:
        return CombinedResponse(error=e.detail)
    except Exception as e:
        return CombinedResponse(error=f"An unexpected server error occurred: {e}")

async def _call_openai_for_json(system_prompt: str, user_prompt: str) -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API call failed: {e}")


async def generate_gap_detection(request: GapDetectionRequest, tone_guideline: str) -> GapDetectionResponse:
    system_prompt = f"""
    You are a strategic advisor helping a professional define their 
    strategic themes. Analyze the context provided below and respond 
    constructively, using the appropriate tone.
    {tone_guideline}
    You MUST return a valid JSON object. Your response should first validate the input.
    If the input is invalid (e.g., nonsensical), return a JSON object with "is_valid": false and an "error_message".
    Otherwise, return "is_valid": true and populate the "analysis" object based on the schema.
    The required JSON schema for the 'analysis' part is: {GapDetectionResponse.model_json_schema()}

    {INSTRUCTIONS}
    """
    user_prompt = f"Here is the business context, please analyze it and provide a response in the required JSON format: {request.model_dump_json()}"
    raw_response = await _call_openai_for_json(system_prompt, user_prompt)
    data = json.loads(raw_response)

    if not data.get("is_valid"):
        raise HTTPException(status_code=400, detail=data.get("error_message", "Invalid input for gap analysis."))
    return GapDetectionResponse(**data.get("analysis", {}))

async def generate_wording_suggestions(request: WordingSuggestionsRequest, tone_guideline: str) -> WordingSuggestionsResponse:
    system_prompt = f"""
    You are a strategic editor. Suggest better wording for the provided themes.
    {tone_guideline}
    You MUST return a valid JSON object. First, validate the input.
    If invalid, return a JSON object with "is_valid": false and "error_message".
    Otherwise, return "is_valid": true and the "analysis" object.
    The required JSON schema for the 'analysis' part is: {WordingSuggestionsResponse.model_json_schema()}

    {INSTRUCTIONS}
    """
    user_prompt = f"Please provide wording suggestions for these themes in the required JSON format: {request.model_dump_json()}"
    raw_response = await _call_openai_for_json(system_prompt, user_prompt)
    data = json.loads(raw_response)

    if not data.get("is_valid"):
        raise HTTPException(status_code=400, detail=data.get("error_message", "Invalid input for wording suggestions."))
    return WordingSuggestionsResponse(**data.get("analysis", {}))



async def generate_goal_mapping(request: GoalMappingRequest, tone_guideline: str) -> GoalMappingResponse:
    system_prompt = f"""
    You are a strategic planner. Map 2–3 specific business goals to each theme.
    {tone_guideline}
    You MUST return a valid JSON object. First, validate the input.
    If invalid, return a JSON with "is_valid": false and an "error_message".
    Otherwise, return "is_valid": true and the "analysis" object.
    The required JSON schema for the 'analysis' part is: {GoalMappingResponse.model_json_schema()}

    {INSTRUCTIONS}
    """
    user_prompt = f"Please map goals to these themes in the required JSON format: {request.model_dump_json()}"
    raw_response = await _call_openai_for_json(system_prompt, user_prompt)
    data = json.loads(raw_response)

    if not data.get("is_valid"):
        raise HTTPException(status_code=400, detail=data.get("error_message", "Invalid input for goal mapping."))
    return GoalMappingResponse(**data.get("analysis", {}))
