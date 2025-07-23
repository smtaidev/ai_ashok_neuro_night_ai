# app/api/endpoints/trend_summary.py

from fastapi import APIRouter, Body, HTTPException
from app.api.models.trend_summary_model import TrendDataInput, TrendCombinedResponse
from app.services import trend_summary_service

router = APIRouter()

@router.post(
    "/analyze",
    response_model=TrendCombinedResponse,
    summary="Generate Trend Summary & Top 3 Trends",
    tags=["Trends Analysis"]
)
async def analyze_trends(
    trend_data: TrendDataInput = Body(..., example={
        "customer_insights": [
            {"question": "What are the evolving needs and preferences of our target customers?", "answer": "Customers now prefer sustainable products and faster, personalized digital experiences.", "impact": "High"},
            {
            "question": "How are customer expectations shifting post-pandemic?",
            "answer": "There is a growing demand for flexible service options, remote support, and enhanced health and safety standards.",
            "impact": "Medium"
            }

        ],
        "competitor_landscape": [
            {"question": "Who are our main competitors?", "answer": "A new startup, 'Innovate Inc.', has entered the market with a low-cost subscription model.", "impact": "Medium"}
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
        "on_the_radar": [
        {
            "question": "Please enter any emerging trends that are currently not apparent, but you would like to monitor as early warnings to prepare your company for them when the time is right",
            "answer": "There is a growing shift in user expectations toward fully personalized digital experiences, potentially driven by advancements in AI-generated content and real-time behavioral analytics. While still in early stages, this could redefine how SaaS platforms engage with users.",
            "impact": "High"
        }
        ]
    })                          
):
    """
    Accepts data from all 12 trend sections and returns a structured, three-part AI-generated summary.
    """
    response = await trend_summary_service.generate_combined_summary_and_trends(trend_data)
    return response