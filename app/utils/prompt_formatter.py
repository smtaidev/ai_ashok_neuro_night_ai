# app/utils/prompt_formatter.py

from app.api.models.trend_summary_model import TrendDataInput


def format_trend_data(data: TrendDataInput) -> str:
    section_titles = {
        "customer_insights": "Customer Insights", "competitor_landscape": "Competitor Landscape",
        "technological_advances": "Technological Advances", "regulatory_and_legal": "Regulatory and Legal Factors",
        "economic_considerations": "Economic Considerations", "supply_chain_logistics": "Supply Chain and Logistics",
        "global_market_trends": "Global Market Trends", "environmental_social_impact": "Environmental and Social Impact",
        "collaboration_partnerships": "Collaboration and Partnerships", "scenarios_risk_assessment": "Scenarios and Risk Assessment",
        "emerging_markets_opportunities": "Emerging Markets and Opportunities", "on_the_radar": "On The Radar (Early Warnings)"
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
