# api/services/swot_service.py

from openai import AsyncOpenAI
import json
import re
from ..core.config import settings
from ..api.models.swot_model import SWOTDataInput, SWOTAnalysisResponse, SWOTScore, SWOTRecommendation
from ..memory import store


client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

def _format_swot_data_for_prompt(data: SWOTDataInput) -> str:
    """Format SWOT data for AI prompt."""
    prompt_text = "SWOT ANALYSIS INPUT DATA:\n\n"
    
    categories = [
        ("Strengths", data.strengths),
        ("Weaknesses", data.weaknesses),
        ("Opportunities", data.opportunities),
        ("Threats", data.threats)
    ]
    
    for category_name, items in categories:
        if items:
            prompt_text += f"{category_name}:\n"
            for item in items:
                prompt_text += f"- {item}\n"
            prompt_text += "\n"
    
    return prompt_text

def _parse_swot_scores(text: str) -> SWOTScore:
    """Parse AI response to extract percentage scores for each SWOT category."""
    try:
        # Expect JSON structure for scores
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON found in response")
        
        data = json.loads(json_match.group(0))
        scores = data.get("scores", {})
        
        return SWOTScore(
            strengths_percentage=float(scores.get("strengths", 25.0)),
            weaknesses_percentage=float(scores.get("weaknesses", 25.0)),
            opportunities_percentage=float(scores.get("opportunities", 25.0)),
            threats_percentage=float(scores.get("threats", 25.0))
        )
    except Exception:
        return SWOTScore(
            strengths_percentage=25.0,
            weaknesses_percentage=25.0,
            opportunities_percentage=25.0,
            threats_percentage=25.0
        )

def _parse_swot_recommendations(text: str) -> SWOTRecommendation:
    """Parse AI response to extract recommendations for each SWOT category."""
    try:
        # Expect JSON structure and parse it directly
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON found in response")
        
        data = json.loads(json_match.group(0))
        recommendations = data.get("recommendations", {})
        
        # Format recommendations as a single string with numbered points and newlines
        for category in ["strengths", "weaknesses", "opportunities", "threats"]:
            if category in recommendations:
                # Remove numbered prefixes and format as a single string
                cleaned_recs = [
                    re.sub(r'^\d+\.\s*', '', rec).strip() 
                    for rec in recommendations[category]
                ]
                # Ensure 3-4 recommendations, fill with defaults if needed
                if not isinstance(cleaned_recs, list) or len(cleaned_recs) < 3:
                    cleaned_recs = ["No specific recommendations available."] * 3
                # Add numbered prefixes back for readability in the output string
                recommendations[category] = "\n".join(
                    f"{i+1}. {rec}" for i, rec in enumerate(cleaned_recs[:4])
                )
            else:
                recommendations[category] = "\n".join(
                    f"{i+1}. No specific recommendations available." for i in range(3)
                )
        
        return SWOTRecommendation(
            strengths_recommendation=recommendations["strengths"],
            weaknesses_recommendation=recommendations["weaknesses"],
            opportunities_recommendation=recommendations["opportunities"],
            threats_recommendation=recommendations["threats"]
        )
    except Exception:
        return SWOTRecommendation(
            strengths_recommendation="\n".join(f"{i+1}. Error parsing recommendations." for i in range(3)),
            weaknesses_recommendation="\n".join(f"{i+1}. Error parsing recommendations." for i in range(3)),
            opportunities_recommendation="\n".join(f"{i+1}. Error parsing recommendations." for i in range(3)),
            threats_recommendation="\n".join(f"{i+1}. Error parsing recommendations." for i in range(3))
        )

async def generate_swot_analysis(data: SWOTDataInput) -> SWOTAnalysisResponse:
    """Generate SWOT analysis with AI-estimated scores and recommendations."""
    
    # Store the latest SWOT input in memory
    store.last_swot_input = data
    
    # Format data for AI prompt
    formatted_data = _format_swot_data_for_prompt(data)
    
    system_prompt = """
    You are a seasoned business consultant with deep expertise in SWOT analysis, delivering insights as if presenting to a board or executive team. Your role is to provide clear, concise, and actionable recommendations that feel professional yet approachable. Based on the provided SWOT data, deliver a structured analysis with:

    1. **Percentage Scores**: Assign a percentage score (0-100%) to each SWOT category (Strengths, Weaknesses, Opportunities, Threats) based on:
       - Strategic significance of each factor
       - Potential impact on business performance
       - Urgency and priority of addressing each area
       - Overall balance of the business situation
       Ensure scores reflect a realistic assessment and add up to a meaningful distribution (not necessarily 100%).

    2. **Actionable Recommendations**: Provide exactly 3-4 concise, specific, and unique recommendations for each category. Each recommendation should:
       - Directly address the provided SWOT items
       - Be actionable, business-focused, and concise (1 sentence)
       - Avoid overlap with other categories
       - Be prefixed with a numbered point (e.g., "1.", "2.") for a structured, executive feel

    **Output Format**:
    Return the response as valid JSON, exactly as follows, with no additional text, markdown, bullet points, or formatting symbols outside the JSON structure:

    ```json
    {
      "scores": {
        "strengths": <X>,
        "weaknesses": <Y>,
        "opportunities": <Z>,
        "threats": <W>
      },
      "recommendations": {
        "strengths": ["1. Recommendation 1", "2. Recommendation 2", "3. Recommendation 3", "4. Recommendation 4"],
        "weaknesses": ["1. Recommendation 1", "2. Recommendation 2", "3. Recommendation 3"],
        "opportunities": ["1. Recommendation 1", "2. Recommendation 2", "3. Recommendation 3", "4. Recommendation 4"],
        "threats": ["1. Recommendation 1", "2. Recommendation 2", "3. Recommendation 3"]
      }
    }
    ```

    **Guidelines**:
    - Use a professional, executive tone, as if presenting to a board.
    - Ensure recommendations are distinct, concise, and tailored to the provided data.
    - Avoid redundancy or overlap across categories (e.g., don't repeat phrases like "research and identify").
    - Prefix each recommendation with a numbered point (e.g., "1.", "2.") for a structured, consultant-like feel.
    - Ensure the JSON output is valid, with scores as numbers (e.g., 80) and recommendations as arrays of strings with numbered prefixes.
    - Do not include any text, bullet points, or markdown symbols outside the JSON structure.
    """
    
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": formatted_data}
            ],
            temperature=0.4,
            max_tokens=1500
        )
        
        analysis_text = response.choices[0].message.content
        
        # Parse scores and recommendations
        scores = _parse_swot_scores(analysis_text)
        recommendations = _parse_swot_recommendations(analysis_text)
        
        return SWOTAnalysisResponse(
            scores=scores,
            recommendations=recommendations,
        )
        
    except Exception as e:
        return SWOTAnalysisResponse(
            scores=SWOTScore(
                strengths_percentage=25.0,
                weaknesses_percentage=25.0,
                opportunities_percentage=25.0,
                threats_percentage=25.0
            ),
            recommendations=SWOTRecommendation(
                strengths_recommendation="\n".join(f"{i+1}. Error generating recommendations." for i in range(3)),
                weaknesses_recommendation="\n".join(f"{i+1}. Error generating recommendations." for i in range(3)),
                opportunities_recommendation="\n".join(f"{i+1}. Error generating recommendations." for i in range(3)),
                threats_recommendation="\n".join(f"{i+1}. Error generating recommendations." for i in range(3))
            )
        )