# app/services/swot_service2.py

import json
from openai import AsyncOpenAI

from ..core.config import settings
from ..core.AI_models import MODEL, TEMPERATURE, MAX_TOKENS
from app.api.models.swot_model2 import (
    SWOTAnalysisRequestV2,
    SWOTAnalysisResponseV2,
    SWOTScoresWithRationale,
    SWOTScoreItem,
    SWOTRecommendationsV2,
)

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

def _format_contextual_prompt(request: SWOTAnalysisRequestV2) -> str:
    """Formats the SWOT data and all available context for the AI prompt."""
    prompt = "## SWOT ANALYSIS INPUT DATA\n\n"

    # Format core SWOT data
    swot = request.swot
    prompt += "### Strengths\n" + "\n".join(f"- {s}" for s in swot.strengths) + "\n\n"
    prompt += "### Weaknesses\n" + "\n".join(f"- {w}" for w in swot.weaknesses) + "\n\n"
    prompt += "### Opportunities\n" + "\n".join(f"- {o}" for o in swot.opportunities) + "\n\n"
    prompt += "### Threats\n" + "\n".join(f"- {t}" for t in swot.threats) + "\n\n"

    # Format optional context
    if request.context:
        prompt += "## ADDITIONAL STRATEGIC CONTEXT\n\n"
        
        if request.context.vision:
            prompt += f"### Company Vision\n- {request.context.vision.vision_statement}\n\n"

        if request.context.challenges:
            prompt += "### Key Challenges\n"
            for challenge in request.context.challenges:
                prompt += f"- **{challenge.title}** (Risk Score: {challenge.risk_score}/100): {challenge.description}\n"
            prompt += "\n"

        if request.context.trends:
            # For brevity, we can summarize trends or list key ones
            prompt += "### Market & Industry Trends\n(The following is based on trend analysis data provided)\n"
            trends_data = request.context.trends.model_dump(exclude_unset=True)
            for category, items in trends_data.items():
                if isinstance(items, list) and items:
                    prompt += f"- **{category.replace('_', ' ').title()}**: Key insights derived from this area.\n"
            prompt += "\n"

    return prompt

async def generate_contextual_swot_analysis(request: SWOTAnalysisRequestV2) -> SWOTAnalysisResponseV2:
    """
    Generates a contextual SWOT analysis using AI, considering vision, challenges, and themes.
    """
    formatted_prompt = _format_contextual_prompt(request)
    
    system_prompt = """
    You are a world-class strategic consultant providing a deep-dive SWOT analysis to an executive team. Your analysis must be interconnected, linking the core SWOT elements with the provided strategic context (vision, challenges, etc.).

    **Your Task:**
    Based on the user's SWOT data and additional context, you will produce a JSON output with two main sections: `scores` and `recommendations`.

    1.  **Scores (1.0-10.0 scale):**
        - For each SWOT category, provide a `value` score from 1.0 to 10.0, reflecting its strategic weight and importance *in light of the provided context*.
        - Provide a concise `rationale` for each score, explaining *why* it was assigned that value, explicitly mentioning the context. For example, "Strengths score high because they directly support the company vision of X."

    2.  **Recommendations (3 per category):**
        - Provide exactly three concise, actionable, and specific recommendations for each SWOT category.
        - These recommendations MUST be contextual. They should show how to leverage a strength to pursue the vision, how to mitigate a weakness, how to seize an opportunity that aligns with trends, or how to neutralize a threat to a key challenge.

    Instruction1:
    SCENARIO A: SWOT Only (No Context) 
        You are a strategic advisor. A user has entered the following SWOT 
        (Strengths, Weaknesses, Opportunities, Threats). Please: 
        1. Assign a score (0–10) to each category, based on how strong or 
        concerning the items appear. - Strengths & Opportunities: Higher = more competitive advantage or 
        potential - Weaknesses & Threats: Higher = more risk or concern 
        2. Write a 1–2 sentence rationale per score. 
        3. Generate 3–4 strategic recommendations per category that are: - Practical - Insightful - Relevant to the inputs (no assumptions about company vision or 
        goals) 
        Be precise and use clear language. Return the output in structured 
        JSON as shown.
        
    Instruction2:
    
     SCENARIO B: SWOT + Strategic Context 
        You are a strategic advisor for a business team. Below is a SWOT 
        analysis, along with related strategic context. 
        Please: 
        1. Score each SWOT category (0–10) based on its content, clarity, and 
        impact in context. 
        2. Write a rationale for each score (1–2 sentences). 
        3. Generate 3–4 strategic recommendations per quadrant. Align insights 
        with the company’s vision, challenges, trends, and goals where 
        applicable. 
        4. If helpful, break suggestions into: - Quick Wins 
        - Long-Term Considerations - Risks to Monitor 
        Use an executive-ready tone. Do not reference missing data or make 
        assumptions. 
        **Context Provided:** - Vision: {if available} - Strategic Goals: {if available} - Themes: {if available} - Key Challenges: {if available} - Trends: {if available} 
        **SWOT:** 
        Strengths: {list} 
        Weaknesses: {list} 
        Opportunities: {list} 
        Threats: {list} 
    
    **CRITICAL: Output Format**
    You MUST return ONLY a valid JSON object matching this exact structure. Do not include any introductory text, markdown formatting like ```json, or any other characters outside the JSON structure.

    ```json
    {
      "scores": {
        "strengths": {
          "value": <float>,
          "rationale": "<string>"
        },
        "weaknesses": {
          "value": <float>,
          "rationale": "<string>"
        },
        "opportunities": {
          "value": <float>,
          "rationale": "<string>"
        },
        "threats": {
          "value": <float>,
          "rationale": "<string>"
        }
      },
      "recommendations": {
        "strengths": ["<recommendation_1>", "<recommendation_2>", "<recommendation_3>"],
        "weaknesses": ["<recommendation_1>", "<recommendation_2>", "<recommendation_3>"],
        "opportunities": ["<recommendation_1>", "<recommendation_2>", "<recommendation_3>"],
        "threats": ["<recommendation_1>", "<recommendation_2>", "<recommendation_3>"]
      }
    }
    ```
    """

    try:
        response = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": formatted_prompt}
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            response_format={"type": "json_object"} # Use JSON mode for reliability
        )

        response_text = response.choices[0].message.content
        analysis_data = json.loads(response_text)
        
        # Validate and structure the response using Pydantic models
        return SWOTAnalysisResponseV2.model_validate(analysis_data)

    except Exception as e:
        # Fallback in case of AI or parsing errors
        error_message = f"Failed to generate contextual SWOT analysis: {str(e)}"
        return SWOTAnalysisResponseV2(
            scores=SWOTScoresWithRationale(
                strengths=SWOTScoreItem(value=0.0, rationale="Error during analysis."),
                weaknesses=SWOTScoreItem(value=0.0, rationale="Error during analysis."),
                opportunities=SWOTScoreItem(value=0.0, rationale="Error during analysis."),
                threats=SWOTScoreItem(value=0.0, rationale="Error during analysis.")
            ),
            recommendations=SWOTRecommendationsV2(
                strengths=["Could not generate recommendations."],
                weaknesses=["Could not generate recommendations."],
                opportunities=["Could not generate recommendations."],
                threats=["Could not generate recommendations."]
            ),
            error=error_message
        )