from openai import AsyncOpenAI
import json
import re
from ..core.config import settings
from ..api.models.trend_summary_model import TrendDataInput, TrendSummaryResponse, TrendCombinedResponse
from ..memory import store  

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

def _parse_summary_response(text: str) -> TrendSummaryResponse:
    """Parse AI response to extract summary sections in JSON format."""
    try:
        # Expect JSON structure for summary
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON found in response")

        data = json.loads(json_match.group(0))
        summary = data.get("summary", {})
        irrelevant_answers = data.get("irrelevant_answers", [])

        return TrendSummaryResponse(
            key_opportunities=summary.get("key_opportunities", "N/A"),
            strengths=summary.get("strengths", "N/A"),
            significant_risks=summary.get("significant_risks", "N/A"),
            challenges=summary.get("challenges", "N/A"),
            strategic_recommendations=summary.get("strategic_recommendations", "N/A"),
            irrelevant_answers=irrelevant_answers
        )
    except Exception:
        return TrendSummaryResponse(
            key_opportunities="Error: Could not parse opportunities and strengths.",
            strengths="Error: Could not parse strengths.",
            significant_risks="Error: Could not parse risks and challenges.",
            challenges="Error: Could not parse challenges.",
            strategic_recommendations="Error: Could not parse recommendations.",
            irrelevant_answers=["Error parsing irrelevant answers."]
        )

async def generate_combined_summary_and_trends(data: TrendDataInput) -> TrendCombinedResponse:
    # Store input in memory for /top-trends fallback
    store.last_trend_input = data

    # Step 1: Format full input and generate general summary + trends
    formatted_data = _format_data_for_prompt(data)

    system_prompt = """
        You are an expert business consultant with extensive experience in strategic planning, market trends, and innovation. Your task is to analyze TRENDS ASSESSMENT RAW DATA and deliver insights as a senior consultant would in a real business setting.

        **General Instructions:**
        - Only analyze answers that are clearly business-related (i.e., relevant to strategy, market trends, or innovation).
        - Ignore answers like 'I don't know'.
        - If an answer is irrelevant, nonsensical, or not business-related (e.g., 'I love movies', 'tell me a joke', 'Trump is the US president', 'My favorite color is blue'), do NOT include it in the summary.
        - Instead, add this message to the 'irrelevant_answers' list:  
        - \"In response to the question '{question}', the provided answer '{answer}' was not relevant to business strategy, market trends, or innovation. Please provide a more relevant answer.\"
        - If all answers in a section are irrelevant or the input is empty, skip that section in the summary.
        - If the entire input contains no relevant answers, return an error message in the summary.

        **Section-Based Analysis:**
        - For each section of trend data:
        - If the input is irrelevant or not business-related, respond with:  
            - \"The input for this section appears to be irrelevant or not business-related. Please provide more relevant information.\"
        - If the data is business-relevant, analyze it and include it in your summary.

        **Executive Summary Structure:**
        Provide a structured summary with the following sections:
        1. **Key Opportunities**
        2. **Strengths**
        3. **Significant Risks**
        4. **Challenges**

        **Strategic Recommendations:**
        - Base your recommendations on the data provided.
        - Reference specific trends or examples.
        - Ensure recommendations are actionable, evidence-based, and appropriate for business leaders.
        - Avoid generic statements. Use clear, professional language.
        - Structure your output as if presenting to a board or executive team.

        **Trend Extraction:**
        - Identify and list the **Top 3 Emerging Trends** based on strategic relevance and frequency.

        **Response Format:**
        Return your analysis using the exact structure below:

        ```json
        {
        "summary": {
            "key_opportunities": "...",
            "strengths": "...",
            "significant_risks": "...",
            "challenges": "...",
            "strategic_recommendations": "..."
        },
        "top_trends": [
            "Trend 1",
            "Trend 2",
            "Trend 3"
        ],
        "irrelevant_answers": [
            "In response to the question '{question}', the provided answer '{answer}' was not relevant to business strategy, market trends, or innovation. Please provide a more relevant answer."
        ]
        }
    """
    try:
        result = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": formatted_data}
            ],
            temperature=0.4,
            max_tokens=1000
        )

        raw_response = result.choices[0].message.content.strip()

        # Parse summary + trends
        parsed_response = _parse_combined_response(raw_response)

        # Step 2: Generate radar analysis from [on_the_radar](http://_vscodecontentref_/0) section
        radar_summary, radar_recommendations = await generate_radar_analysis(data)

        return TrendCombinedResponse(
            summary=parsed_response.summary,
            top_trends=parsed_response.top_trends,
            radar_executive_summary=radar_summary,
            radar_recommendation=radar_recommendations
        )

    except Exception as e:
        return TrendCombinedResponse(
            summary=TrendSummaryResponse(
                key_opportunities="Error generating summary.",
                strengths=str(e),
                significant_risks="Check logs.",
                challenges="Check logs.",
                strategic_recommendations="Check logs.",
                irrelevant_answers=["Error generating summary."]
            ),
            top_trends=["Error generating trends."],
            radar_executive_summary=["Error analyzing early signals."],
            radar_recommendation=["N/A"]
        )

def _parse_combined_response(text: str) -> TrendCombinedResponse:
    try:
        # Expect JSON structure for the entire response
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON found in response")

        data = json.loads(json_match.group(0))
        trends = data.get("top_trends", [])

        # Use _parse_summary_response to parse the summary section
        summary = _parse_summary_response(text)

        return TrendCombinedResponse(
            summary=summary,
            top_trends=trends[:3] if isinstance(trends, list) else ["Error parsing top trends."]
        )

    except Exception:
        return TrendCombinedResponse(
            summary=TrendSummaryResponse(
                key_opportunities="Error parsing summary.",
                strengths="Error parsing strengths.",
                significant_risks="Error parsing risks.",
                challenges="Error parsing challenges.",
                strategic_recommendations="Check raw LLM response.",
                irrelevant_answers=["Error parsing summary."]
            ),
            top_trends=["Error parsing top trends."]
        )

async def generate_radar_analysis(data: TrendDataInput) -> tuple[list[str], list[str]]:
    radar_entries = data.on_the_radar
    if not radar_entries:
        return [], []

    radar_prompt = "You are an innovation strategist. Analyze the following early warning trend signals:\n\n"
    for item in radar_entries:
        if item.answer:
            radar_prompt += f"Q: {item.question}\nA: {item.answer}\nImpact: {item.impact}\n\n"

    radar_prompt += (
        "Now write:\n"
        "1. A short summary explaining the strategic implications.\n"
        "2. A short list (2–3) of strategic recommendations.\n\n"
        "FORMAT:\n"
        "Summary:\n- ...\n\nRecommendations:\n- ...\n- ..."
    )

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an innovation strategist."},
            {"role": "user", "content": radar_prompt}
        ],
        temperature=0.4,
        max_tokens=600,
    )

    content = response.choices[0].message.content.strip()

    # Parse sections
    summary_lines = []
    recommendation_lines = []
    summary_started = False
    recommendation_started = False

    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.lower().startswith("summary"):
            summary_started = True
            recommendation_started = False
            continue
        if line.lower().startswith("recommendation"):
            summary_started = False
            recommendation_started = True
            continue
        if summary_started:
            summary_lines.append(line.strip("- ").strip())
        if recommendation_started:
            recommendation_lines.append(line.strip("- ").strip())

    return summary_lines, recommendation_lines