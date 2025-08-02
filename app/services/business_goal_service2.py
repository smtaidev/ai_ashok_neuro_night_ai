# app/services/business_goal_service2.py

import json
from openai import AsyncOpenAI
from typing import Dict

from ..core.config import settings
from ..core.AI_models import MODEL, TEMPERATURE
# Make sure to import the models
from ..api.models.business_goal_model2 import BusinessGoalAnalysisRequest, BusinessGoalAnalysisResponse, DashboardInsights
from ..utils.Tone import TONE_GUIDELINES

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

def _format_prompt_for_goal_analysis(request: BusinessGoalAnalysisRequest) -> str:
    """Formats the business goals and strategic context into a clear text prompt."""

    prompt = "## STRATEGIC CONTEXT\n"
    prompt += f"- **Vision:** {request.vision}\n"

    # Detailed Strategic Themes
    prompt += "- **Strategic Themes:**\n"
    for i, theme in enumerate(request.strategic_themes, 1):
        prompt += f"  {i}. {theme.name} — {theme.description}\n"

    # Detailed Challenges
    prompt += "- **Key Challenges:**\n"
    for i, challenge in enumerate(request.challenges, 1):
        prompt += (
            f"  {i}. {challenge.title}\n"
            f"     - Category: {challenge.category}\n"
            f"     - Impact on Business: {challenge.impact_on_business}\n"
            f"     - Ability to Address: {challenge.ability_to_address}\n"
            f"     - Risk Score: {challenge.risk_score}\n"
            f"     - Description: {challenge.description}\n"
        )

    prompt += "\n## BUSINESS GOALS FOR ANALYSIS\n\n"
    for i, goal in enumerate(request.goals, 1):
        prompt += f"### Goal {i}: {goal.title}\n"
        prompt += f"- **Description:** {goal.description}\n"
        prompt += f"- **Related Theme:** {goal.related_strategic_theme}\n"
        prompt += f"- **Priority:** {goal.priority}\n"
        prompt += f"- **Resource Readiness:** {goal.resource_readiness}\n"
        prompt += f"- **Impacts:** "
        prompt += f"Risks ({goal.impact_ratings.risks}), "
        prompt += f"Compliance ({goal.impact_ratings.compliance}), "
        prompt += f"Change Management ({goal.impact_ratings.change_management}) \n\n"

    return prompt


async def analyze_business_goals(request: BusinessGoalAnalysisRequest) -> BusinessGoalAnalysisResponse:
    """
    Analyzes a portfolio of business goals against strategic context using an AI model.
    First, it validates the input for relevance before proceeding with the analysis.
    """
    user_prompt = _format_prompt_for_goal_analysis(request)
    tone_instruction = TONE_GUIDELINES.get(request.tone, TONE_GUIDELINES["advisor"])

    # Define a schema that includes our validation fields
    # This tells the AI how to structure its response for both validation and analysis
    validation_and_analysis_schema = {
        "type": "object",
        "properties": {
            "is_input_valid": {"type": "boolean"},
            "validation_error_message": {
                "type": "string", 
                "description": "If input is invalid, explain which goal is problematic and why. Otherwise, this should be null."
            },
            "analysis": BusinessGoalAnalysisResponse.model_json_schema()
        },
        "required": ["is_input_valid", "validation_error_message"]
    }

    system_prompt = f"""
    You are an expert Chief Strategy Officer. {tone_instruction} You have two critical tasks.

    **TASK 1: VALIDATE INPUT**
    First, you MUST examine the `title` and `description` of EACH goal provided by the user. If ANY goal contains clearly non-business-related content (e.g., "tell me a joke," random gibberish, personal notes), you must stop immediately.
    - If input is INVALID: Set `is_input_valid` to `false` and provide a clear reason in `validation_error_message`. The `analysis` field should be null.
    - If all inputs are VALID: Set `is_input_valid` to `true` and `validation_error_message` to null. Then, proceed to Task 2.

    **TASK 2: PERFORM STRATEGIC ANALYSIS (only if input is valid)**
    If validation passes, analyze the portfolio of business goals against the company's strategic context (vision, themes, challenges) and populate the `analysis` object with the following:
    1.  **Alignment Summary:** A holistic summary of how the goals align with the vision/themes and address challenges.
    2.  **SMART Suggestions:** For each goal, provide a recommendation to make it more Specific, Measurable, Achievable, Relevant, and Time-bound.
    3.  **Strategic Priorities:** Identify the top 2-3 most critical goals.
    4.  **Strategic Fit Scores:** For each goal, provide a score (0-100) and a brief comment justifying it.
    5.  **Execution Watchouts:** Identify the biggest execution risks or red flags across the portfolio.
    6.  **Dashboard Insights:** Synthesize insights for each category based on all provided goal data.

    **CRITICAL OUTPUT INSTRUCTIONS:**
    Your response MUST be ONLY a single, valid JSON object conforming to this exact schema. Do not include any text or markdown outside the JSON structure.
    {json.dumps(validation_and_analysis_schema, indent=2)}
    """

    try:
        response = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=TEMPERATURE,
            response_format={"type": "json_object"}
        )
        
        response_data = json.loads(response.choices[0].message.content)

        # --- NEW VALIDATION LOGIC ---
        if not response_data.get("is_input_valid"):
            error_msg = response_data.get("validation_error_message", "An input goal was deemed irrelevant for business analysis.")
            # Return the standard response model with the error field populated
            return BusinessGoalAnalysisResponse(
                alignment_summary="", smart_suggestions=[], strategic_priorities=[],
                strategic_fit_scores=[], execution_watchouts=[],
                dashboard_insights=DashboardInsights(risks=[], regulatory_compliances=[], roadblocks=[], talent=[], culture_realignment=[], change_management=[], learning_and_development=[]),
                error=error_msg
            )
        
        # If valid, parse the nested 'analysis' object
        analysis_payload = response_data.get("analysis")
        if not analysis_payload:
             raise ValueError("AI returned a valid flag but no analysis payload.")

        return BusinessGoalAnalysisResponse.model_validate(analysis_payload)

    except Exception as e:
        error_message = f"An error occurred during AI processing: {str(e)}"
        # Return a valid response model with the error field populated for any exception
        return BusinessGoalAnalysisResponse(
            alignment_summary="", smart_suggestions=[], strategic_priorities=[],
            strategic_fit_scores=[], execution_watchouts=[],
            dashboard_insights=DashboardInsights(risks=[], regulatory_compliances=[], roadblocks=[], talent=[], culture_realignment=[], change_management=[], learning_and_development=[]),
            error=error_message
        )