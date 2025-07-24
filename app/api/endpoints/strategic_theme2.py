from fastapi import APIRouter, Body, HTTPException
from typing import Dict
from app.services import strategic_theme2_service as service
from app.api.models.strategic_theme2_model import *

router = APIRouter()

# --- Example Data Payloads (as they were) ---
gap_detection_example = {
  "themes": [
    {"name": "Digital Transformation", "description": "Modernize core infrastructure."},
    {"name": "Enhance Customer Experience", "description": "Improve support response times."}
  ],
  "context": {
    "vision": "To become the leading provider of sustainable packaging solutions.",
    "swot": {"strengths": ["Strong brand reputation"],"weaknesses": ["Limited international presence"],"opportunities": ["Growing market for eco-friendly products"],"threats": ["Rising raw material costs"]},
    "challenges": [{"title": "Supply Chain Volatility","category": "Operations","impact_on_business": "high","ability_to_address": "moderate","description": "Raw material prices are unpredictable.","risk_score": 85}]
  }
}
wording_suggestions_example = {"themes": [{"name": "Make Things Better", "description": "Improve our stuff."}]}
goal_mapping_example = {"themes": [{"name": "Operational Excellence", "description": "Streamline internal processes."}]}
benchmarking_example = {"profile": {"industry": "B2B SaaS", "size": "50-200 Employees", "businessModel": "Subscription"}}

# --- API Endpoints with Full Implementation ---
@router.post("/gap-detection", response_model=GapDetectionResponse, summary="A. Identify Gaps in Strategic Themes")
async def analyze_gaps(request: GapDetectionRequest = Body(..., example=gap_detection_example)):
    if not request.themes:
        raise HTTPException(status_code=400, detail="At least one strategic theme is required.")
    response = await service.generate_gap_detection(request)
    if isinstance(response, Dict) and "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response

@router.post("/wording-suggestions", response_model=WordingSuggestionsResponse, summary="B. Get Wording Suggestions for Themes")
async def suggest_wording(request: WordingSuggestionsRequest = Body(..., example=wording_suggestions_example)):
    if not request.themes:
        raise HTTPException(status_code=400, detail="At least one strategic theme is required.")
    response = await service.generate_wording_suggestions(request)
    if isinstance(response, Dict) and "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response

@router.post("/goal-mapping", response_model=GoalMappingResponse, summary="C. Map Business Goals to Themes")
async def map_goals(request: GoalMappingRequest = Body(..., example=goal_mapping_example)):
    if not request.themes:
        raise HTTPException(status_code=400, detail="At least one strategic theme is required.")
    response = await service.generate_goal_mapping(request)
    if isinstance(response, Dict) and "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response

@router.post("/benchmarking", response_model=BenchmarkingResponse, summary="D. Benchmark Themes Against Industry Peers")
async def benchmark_themes(request: BenchmarkingRequest = Body(..., example=benchmarking_example)):
    response = await service.generate_benchmarking(request)
    if isinstance(response, Dict) and "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response