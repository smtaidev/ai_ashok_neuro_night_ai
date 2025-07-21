# app/api/endpoints/strategic_theme2.py

from fastapi import APIRouter, Body, HTTPException
from app.services import strategic_theme2_service
from app.api.models.strategic_theme2_model import *

router = APIRouter()

# --- Example Data Payloads ---
# Defining these here keeps the endpoint definitions cleaner.

gap_detection_example = {
    "themes": [
        {"name": "Digital Transformation", "description": "Modernize our core infrastructure and leverage data analytics."},
        {"name": "Enhance Customer Experience", "description": "Improve support response times and personalize user journeys."}
    ],
    "context": {
        "vision": "To become the leading provider of sustainable packaging solutions in North America.",
        "swot": {
            "strengths": ["Strong brand reputation", "Patented recycling technology"],
            "weaknesses": ["Limited international presence", "High dependency on a single supplier"],
            "opportunities": ["Growing market for eco-friendly products", "Potential for government subsidies"],
            "threats": ["Rising raw material costs", "New low-cost competitors"]
        },
        "challenges": [
            "Navigating complex global supply chains",
            "Meeting evolving regulatory standards for sustainability"
        ]
    }
}

wording_suggestions_example = {
    "themes": [
        {"name": "Make Things Better", "description": "We will improve our stuff."},
        {"name": "Sales Initiative", "description": "Try to sell more products to more people."}
    ]
}

goal_mapping_example = {
    "themes": [
        {"name": "Operational Excellence", "description": "Streamline internal processes to reduce waste and improve efficiency."},
        {"name": "Market Expansion", "description": "Enter new geographical markets and customer segments."}
    ]
}

benchmarking_example = {
    "profile": {
        "industry": "B2B SaaS",
        "size": "50-200 Employees",
        "region": "Global",
        "businessModel": "Subscription-based"
    }
}


# --- API Endpoints with Examples ---

@router.post(
    "/gap-detection",
    response_model=GapDetectionResponse,
    summary="A. Identify Gaps in Strategic Themes"
)
async def analyze_gaps(request: GapDetectionRequest = Body(..., example=gap_detection_example)):
    """Analyzes current themes against vision, SWOT, and challenges to find gaps."""
    if not request.themes:
        raise HTTPException(status_code=400, detail="At least one strategic theme is required for gap analysis.")
    return await strategic_theme2_service.generate_gap_detection(request)



@router.post(
    "/wording-suggestions",
    response_model=WordingSuggestionsResponse,
    summary="B. Get Wording Suggestions for Themes"
)
async def suggest_wording(request: WordingSuggestionsRequest = Body(..., example=wording_suggestions_example)):
    """Improves the clarity and impact of theme names and descriptions."""
    if not request.themes:
        raise HTTPException(status_code=400, detail="At least one strategic theme is required for wording suggestions.")
    return await strategic_theme2_service.generate_wording_suggestions(request)




@router.post(
    "/goal-mapping",
    response_model=GoalMappingResponse,
    summary="C. Map Business Goals to Themes"
)
async def map_goals(request: GoalMappingRequest = Body(..., example=goal_mapping_example)):
    """Suggests 2-3 specific business goals for each strategic theme."""
    if not request.themes:
        raise HTTPException(status_code=400, detail="At least one strategic theme is required for goal mapping.")
    return await strategic_theme2_service.generate_goal_mapping(request)

@router.post(
    "/benchmarking",
    response_model=BenchmarkingResponse,
    summary="D. Benchmark Themes Against Industry Peers"
)
async def benchmark_themes(request: BenchmarkingRequest = Body(..., example=benchmarking_example)):
    """Suggests common strategic themes based on the company's profile."""
    return await strategic_theme2_service.generate_benchmarking(request)