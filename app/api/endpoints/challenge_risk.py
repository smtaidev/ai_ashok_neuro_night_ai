# app/api/endpoints/challenge_risk.py


from fastapi import APIRouter, HTTPException, Body
from app.api.models.challenge_model import ChallengeEvaluationRequest, ChallengeRiskScoreResponse
from app.services.challenge_risk_service import evaluate_challenge_risk
from app.api.models.challenge_model import (
    ChallengeRecommendationRequest, 
    ChallengeRecommendationResponse
)
from app.services.challenge_risk_service import generate_challenge_recommendations


router = APIRouter()

@router.post(
    "/evaluate",
    response_model=ChallengeRiskScoreResponse,
    summary="Evaluate Challenge Risk Score",
    tags=["Challenge Risk"]
)
async def assess_challenge_risk(request: ChallengeEvaluationRequest = Body(..., example={
    "challenge": {
        "title": "Inefficient Remote Work Infrastructure",
        "category": "Operations",
        "impact_on_business": "high",
        "ability_to_address": "moderate",
        "description": "The current tools and workflows are not optimized for hybrid work, leading to productivity loss."
    },
    "swot": {
        "strengths": [
            "Strong brand recognition in the market",
            "Experienced management team with 15+ years in industry",
            "Robust financial position with healthy cash flow"
        ],
        "weaknesses": [
            "Limited digital presence compared to competitors",
            "High operational costs due to legacy systems"
        ],
        "opportunities": [
            "Emerging markets expansion potential in Asia",
            "New technology adoption could streamline operations",
            "Strategic partnerships with tech companies"
        ],
        "threats": [
            "Increasing competition from new market entrants",
            "Economic downturn affecting consumer spending",
            "Regulatory changes in key markets"
        ]
    },
    "trends": {
        "customer_insights": [
            {"question": "What are the evolving needs and preferences of our target customers?", 
             "answer": "Customers now prefer sustainable products and faster, personalized digital experiences.", 
             "impact": "High"}
        ],
        "competitor_landscape": [
            {"question": "Who are our main competitors?", 
             "answer": "A new startup, 'Innovate Inc.', has entered the market with a low-cost subscription model.", 
             "impact": "Medium"}
        ],
        "Economic Considerations": [
            {
            "question": "How is the economic environment (e.g., inflation, interest rates) affecting consumer spending and industry growth?",
            "answer": "High inflation and interest rates are reducing consumer discretionary spending, leading to slower growth in sectors like retail and real estate. Some industries are maintaining stability through essential services and adaptive pricing strategies.",
            "impact": "Medium"
            }
        ],
        "technological_advances": [],
        "regulatory_and_legal": [],
        "supply_chain_logistics": [],
        "global_market_trends": [],
        "environmental_social_impact": [],
        "collaboration_partnerships": [],
        "scenarios_risk_assessment": [],
        "emerging_markets_opportunities": [],
        "on_the_radar": []
    }
  })
):
    try:
        return await evaluate_challenge_risk(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating challenge risk: {str(e)}")

@router.post(
    "/recommendations",
    response_model=ChallengeRecommendationResponse,
    summary="Generate Recommendations for High-Risk Challenges",
    tags=["Challenge Risk"]
)
async def recommend_for_challenges(request: ChallengeRecommendationRequest = Body(..., example={
      "challenges": [
        {
        "title": "Outdated IT Infrastructure",
        "category": "Technology",
        "impact_on_business": "high",
        "ability_to_address": "low",
        "description": "Legacy systems are slowing down operations.",
        "risk_score": 87
        },
        {
        "title": "Poor Remote Work Adoption",
        "category": "Operations",
        "impact_on_business": "moderate",
        "ability_to_address": "moderate",
        "description": "Remote collaboration tools are underutilized.",
        "risk_score": 74
        }
    ],
    "swot": {
        "strengths": [
            "Strong brand recognition in the market",
            "Experienced management team with 15+ years in industry",
            "Robust financial position with healthy cash flow"
        ],
        "weaknesses": [
            "Limited digital presence compared to competitors",
            "High operational costs due to legacy systems"
        ],
        "opportunities": [
            "Emerging markets expansion potential in Asia",
            "New technology adoption could streamline operations",
            "Strategic partnerships with tech companies"
        ],
        "threats": [
            "Increasing competition from new market entrants",
            "Economic downturn affecting consumer spending",
            "Regulatory changes in key markets"
        ]
    },
    "trends": {
        "customer_insights": [
            {"question": "What are the evolving needs and preferences of our target customers?", 
             "answer": "Customers now prefer sustainable products and faster, personalized digital experiences.", 
             "impact": "High"}
        ],
        "competitor_landscape": [
            {"question": "Who are our main competitors?", 
             "answer": "A new startup, 'Innovate Inc.', has entered the market with a low-cost subscription model.", 
             "impact": "Medium"}
        ],
        "Economic Considerations": [
            {
            "question": "How is the economic environment (e.g., inflation, interest rates) affecting consumer spending and industry growth?",
            "answer": "High inflation and interest rates are reducing consumer discretionary spending, leading to slower growth in sectors like retail and real estate. Some industries are maintaining stability through essential services and adaptive pricing strategies.",
            "impact": "Medium"
            }
        ],
        "technological_advances": [],
        "regulatory_and_legal": [],
        "supply_chain_logistics": [],
        "global_market_trends": [],
        "environmental_social_impact": [],
        "collaboration_partnerships": [],
        "scenarios_risk_assessment": [],
        "emerging_markets_opportunities": [],
        "on_the_radar": []
    }
})):
    try:
        return await generate_challenge_recommendations(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")