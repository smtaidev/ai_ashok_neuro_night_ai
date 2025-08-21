# app/services/trend_summary_service.py

from openai import AsyncOpenAI
import json
import re
from ..core.config import settings
from ..core.AI_models import MODEL, TEMPERATURE, MAX_TOKENS
from ..api.models.trend_summary_model import TrendDataInput, TrendSummaryResponse, TrendCombinedResponse
from ..memory import store
from ..utils.Tone import TONE_GUIDELINES

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

def _format_data_for_prompt(data: TrendDataInput) -> str:
    section_titles = {
        "customer_insights": "Customer Insights",
        "competitor_landscape": "Competitor Landscape",
        "technological_advances": "Technological Advances",
        "regulatory_and_legal": "Regulatory and Legal Factors",
        "economic_considerations": "Economic Considerations",
        "supply_chain_logistics": "Supply Chain and Logistics",
        "global_market_trends": "Global Market Trends",
        "environmental_social_impact": "Environmental and Social Impact",
        "collaboration_partnerships": "Collaboration and Partnerships",
        "scenarios_risk_assessment": "Scenarios and Risk Assessment",
        "emerging_markets_opportunities": "Emerging Markets and Opportunities",
        "on_the_radar": "On The Radar (Early Warnings)"
    }
    prompt_text = "TRENDS ASSESSMENT RAW DATA:\n\n"
    for field_name, title in section_titles.items():
        answers = getattr(data, field_name, [])
        if answers:
            prompt_text += f"--- {title} ---\n"
            for item in answers:
                if item.answer and item.answer.strip():
                    prompt_text += f"Q: {item.question}\n"
                    prompt_text += f"A: {item.answer}\n"
                    if item.impact:
                        prompt_text += f"Impact: {item.impact}\n"
            prompt_text += "\n"
    return prompt_text

def _parse_combined_response(text: str) -> TrendCombinedResponse:
    """Parse the entire AI JSON response into a TrendCombinedResponse object."""
    try:
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if not json_match:
            return TrendCombinedResponse(
                summary=TrendSummaryResponse(key_opportunities="", strengths="", significant_risks="", challenges="", strategic_recommendations=""),
                error=f"Could not parse AI response, no valid JSON found. Raw response: {text[:500]}"
            )

        data = json.loads(json_match.group(0))

        # Parse the nested summary object
        summary_data = data.get("summary", {})
        summary = TrendSummaryResponse(
            key_opportunities=summary_data.get("key_opportunities", "N/A"),
            strengths=summary_data.get("strengths", "N/A"),
            significant_risks=summary_data.get("significant_risks", "N/A"),
            challenges=summary_data.get("challenges", "N/A"),
            strategic_recommendations=summary_data.get("strategic_recommendations", "N/A"),
            irrelevant_answers=data.get("irrelevant_answers", [])
        )

        # Parse the other top-level fields
        return TrendCombinedResponse(
            summary=summary,
            trend_synthesis=data.get("trend_synthesis", []),
            early_warnings=data.get("early_warnings", "N/A"),
            strategic_opportunities=data.get("strategic_opportunities", []),
            analyst_recommendations=data.get("analyst_recommendations", "N/A")
        )

    except (json.JSONDecodeError, ValueError) as e:
        return TrendCombinedResponse(
            summary=TrendSummaryResponse(key_opportunities="", strengths="", significant_risks="", challenges="", strategic_recommendations=""),
            error=f"Error parsing JSON from AI response: {str(e)}. Raw text: {text[:500]}"
        )
    except Exception as e:
        return TrendCombinedResponse(
            summary=TrendSummaryResponse(key_opportunities="", strengths="", significant_risks="", challenges="", strategic_recommendations=""),
            error=f"An unexpected error occurred during parsing: {str(e)}"
        )

async def generate_combined_summary_and_trends(data: TrendDataInput) -> TrendCombinedResponse:
    store.last_trend_input = data
    formatted_data = _format_data_for_prompt(data)

    tone = data.tone or "coach"
    tone_guideline = TONE_GUIDELINES.get(tone, TONE_GUIDELINES["coach"])  

    system_prompt = f"""
        You are an expert business consultant with extensive experience in strategic planning, market trends, and innovation. Your task is to analyze TRENDS ASSESSMENT RAW DATA and deliver insights as a senior consultant would in a real business setting.

        ### Tone Instructions:
        {tone_guideline}

        ### General Instructions:
        - Analyze only business-related answers relevant to strategy, market trends, or innovation.
        - Ignore answers like 'I don't know' or nonsensical, non-business-related input.
        - If an answer is irrelevant, add a descriptive message to the 'irrelevant_answers' list.
        - If all answers are irrelevant, return an error message in the summary sections.

        ### Part 1: Executive Summary & Synthesis
        Analyze all sections of the raw data to create a holistic view.
        - **Executive Summary:** Structure this with four key sections: Key Opportunities, Strengths, Significant Risks, and Challenges.
        - **Strategic Recommendations:** Provide actionable, evidence-based recommendations based on the data.
        - **Trend Synthesis:** Identify and list the Top 3 Emerging Trends based on their strategic relevance and frequency in the data.

        ### Part 2: Analyst's Briefing
        Adopt the mindset of an analyst delivering a sharp, direct briefing to leadership.
        - **Early Warnings:** Highlight blind spots, underappreciated risks, or mismatched intensity (e.g., an item marked 'Low' impact that is clearly a High-relevance threat).
        - **Strategic Opportunities:** Suggest 2–4 forward-looking ideas or new directions the business could explore based on the trends.
        - **Analyst Recommendations:** State what the leadership team should consider, investigate, or act on based on your interpretation. Be crisp, direct, and avoid filler.

        ### Response Format:
        Return your complete analysis using the exact JSON structure below. Ensure all keys are present.

        ```json
        {{
          "summary": {{
            "key_opportunities": "...",
            "strengths": "...",
            "significant_risks": "...",
            "challenges": "...",
            "strategic_recommendations": "..."
          }},
          "trend_synthesis": [
            "Trend 1: Detailed description of the first major synthesized trend.",
            "Trend 2: Detailed description of the second major synthesized trend.",
            "Trend 3: Detailed description of the third major synthesized trend."
          ],
          "early_warnings": "Concise summary of blind spots, underappreciated risks, or mismatched intensity.",
          "strategic_opportunities": [
            "A forward-looking idea or new direction the business could explore.",
            "Another forward-looking idea or new direction."
          ],
          "analyst_recommendations": "Direct and actionable recommendations for the leadership team.",
          "irrelevant_answers": [
            "In response to the question '{{question}}', the provided answer '{{answer}}' was not relevant to business strategy, market trends, or innovation. Please provide a more relevant answer."
          ]
        }}    """

    try:
        result = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": formatted_data}
            ],
            temperature=TEMPERATURE,
            max_tokens=2048  
        )

        raw_response = result.choices[0].message.content.strip()

        parsed_response = _parse_combined_response(raw_response)

        if parsed_response.error:
            return parsed_response

        radar_summary, radar_recommendations = await generate_radar_analysis(data)

        parsed_response.radar_executive_summary = radar_summary
        parsed_response.radar_recommendation = radar_recommendations

        return parsed_response

    except Exception as e:
        return TrendCombinedResponse(
            summary=TrendSummaryResponse(key_opportunities="", strengths="", significant_risks="", challenges="", strategic_recommendations=""),
            error=f"An error occurred while generating the trend summary: {str(e)}"
        )


async def generate_radar_analysis(data: TrendDataInput) -> tuple[list[str], list[str]]:
    radar_entries = data.on_the_radar
    if not radar_entries:
        return [], []

    radar_prompt = "You are an innovation strategist. Analyze the following early warning trend signals:\n\n"
    for item in radar_entries:
        if item.answer and item.answer.strip():
            radar_prompt += f"Q: {item.question}\nA: {item.answer}\nImpact: {item.impact}\n\n"

    radar_prompt += (
        "Based on these signals, provide:\n"
        "1. A short executive summary explaining the strategic implications.\n"
        "2. A short, actionable list (2–3 items) of strategic recommendations.\n\n"
        "Use the following format exactly:\n"
        "Summary:\n- Bullet point 1\n- Bullet point 2\n\nRecommendations:\n- Recommendation 1\n- Recommendation 2"
    )

    response = await client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an innovation strategist."},
            {"role": "user", "content": radar_prompt}
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )

    content = response.choices[0].message.content.strip()

    summary_lines = []
    recommendation_lines = []
    current_section = None

    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.lower().startswith("summary:"):
            current_section = "summary"
            continue
        if line.lower().startswith("recommendations:"):
            current_section = "recommendations"
            continue

        if current_section == "summary":
            summary_lines.append(line.strip("- ").strip())
        elif current_section == "recommendations":
            recommendation_lines.append(line.strip("- ").strip())

    return summary_lines, recommendation_lines