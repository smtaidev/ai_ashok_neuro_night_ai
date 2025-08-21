# app/services/challenge_risk_service.py

from openai import AsyncOpenAI
from app.api.models.challenge_model import ChallengeEvaluationRequest, ChallengeRiskScoreResponse
from app.core.config import settings

from app.api.models.challenge_model import (
    ChallengeRecommendationRequest, 
    ChallengeRecommendationResponse
)

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def evaluate_challenge_risk(request: ChallengeEvaluationRequest) -> ChallengeRiskScoreResponse:
    challenge = request.challenge
    swot = request.swot
    trends = request.trends

    prompt = f"""
You are a strategic risk evaluation AI.

Evaluate the following business challenge and return a single risk score between 1 and 100, where higher means more risk. Dont provide the risk score if the challenge input (e.g. title or description) is not clear or insufficient, irrelevant information is provided, in that case, just provide NaN value to the risk score.

**Guidelines:**
- Consider the challenge's impact on the business, its category, and the ability to address it.
- Use the SWOT analysis to understand the internal strengths and weaknesses.
- Use the trends analysis to understand external opportunities and threats.
- Provide a concise risk score based on the overall context.
- Do not provide any additional text or explanations, just the risk score.
- Do not use any markdown formatting.
- Do not include any other text in the response.


Challenge Details:
- Title: {challenge.title}
- Category: {challenge.category}
- Description: {challenge.description}
- Impact on Business: {challenge.impact_on_business}
- Ability to Address: {challenge.ability_to_address}

SWOT Context:
- Strengths: {', '.join(swot.strengths)}
- Weaknesses: {', '.join(swot.weaknesses)}
- Opportunities: {', '.join(swot.opportunities)}
- Threats: {', '.join(swot.threats)}

Trends Context:
"""
    for section_name, items in trends.dict().items():
        if items:
            prompt += f"\n--- {section_name.replace('_', ' ').title()} ---\n"
            for item in items:
                if isinstance(item, dict):
                    q = item.get("question", "N/A")
                    a = item.get("answer", "N/A")
                    impact = item.get("impact", "N/A")
                    prompt += f"Q: {q}\nA: {a}\nImpact: {impact}\n"
                else:
                    prompt += f"Note: Unexpected item format: {item}\n"

    prompt += "\n\nReturn ONLY in this format:\nRISK SCORE: [1–100]"

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a business risk analysis expert."},
                  {"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=100
    )

    content = response.choices[0].message.content

    import re
    match = re.search(r"RISK SCORE:\s*(\d+)", content)
    score = int(match.group(1)) if match else 50

    return ChallengeRiskScoreResponse(risk_score=score)



async def generate_challenge_recommendations(
    request: ChallengeRecommendationRequest
) -> ChallengeRecommendationResponse:

    swot = request.swot
    trends = request.trends
    challenges = request.challenges

    prompt = "You are a business strategy consultant. You are tasked with providing strategic recommendations for the organization's top challenges.\n\n"

    prompt += "CHALLENGES:\n"
    for i, ch in enumerate(challenges, 1):
        prompt += f"{i}. Title: {ch.title}\n"
        prompt += f"   Category: {ch.category}\n"
        prompt += f"   Risk Score: {ch.risk_score}\n"
        prompt += f"   Description: {ch.description}\n"

    prompt += "\nSWOT:\n"
    prompt += f"- Strengths: {', '.join(swot.strengths)}\n"
    prompt += f"- Weaknesses: {', '.join(swot.weaknesses)}\n"
    prompt += f"- Opportunities: {', '.join(swot.opportunities)}\n"
    prompt += f"- Threats: {', '.join(swot.threats)}\n"

    prompt += "\nTRENDS:\n"
    for section_name, items in trends.dict().items():
        if items:
            prompt += f"\n--- {section_name.replace('_', ' ').title()} ---\n"
            for item in items:
                if isinstance(item, dict):
                    q = item.get("question", "N/A")
                    a = item.get("answer", "N/A")
                    impact = item.get("impact", "N/A")
                    prompt += f"Q: {q}\nA: {a}\nImpact: {impact}\n"
                else:
                    prompt += f"Note: Unexpected item format: {item}\n"

    prompt += """
Now, based on the given challenges, SWOT, and Trend analysis above — generate a concise and strategic list of recommendations.
Your response should address the most critical issues and propose high-level business actions.

**Guidelines:**
- Focus on actionable recommendations that can be implemented by the organization.
- Prioritize recommendations based on the risk scores of the challenges.
- Ensure recommendations are clear, concise, and directly related to the challenges.
- Avoid generic advice; tailor recommendations to the specific challenges and context provided.
- Use bullet points for clarity.
- If the challenges are not clear or insufficient information is provided, state that no recommendations can be generated.
- If the SWOT or Trend analysis is lacking, indicate that as well.
 

Return output in this format:

RECOMMENDATIONS:
- [Recommendation 1]
- [Recommendation 2]
- ...
    """

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a strategic business advisor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=800
    )

    content = response.choices[0].message.content

    import re
    match = re.search(r"RECOMMENDATIONS:\s*(.*)", content, re.DOTALL)
    rec_text = match.group(1).strip() if match else "No recommendations generated."

    return ChallengeRecommendationResponse(recommendations=rec_text)