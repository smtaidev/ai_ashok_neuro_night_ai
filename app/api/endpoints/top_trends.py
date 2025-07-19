# from fastapi import APIRouter, Body
# from app.api.models.trend_summary_model import TrendDataInput
# from app.api.models.top_trends_model import TopTrendsResponse
# from app.services import top_trends_service

# router = APIRouter()

# @router.post(
#     "/top-trends",
#     response_model=TopTrendsResponse,
#     summary="Get Top 3 Trends from raw data",
#     tags=["Trends Analysis"]
# )
# async def get_top_trends(
#     trend_data: TrendDataInput = Body(...)):
#     return await top_trends_service.generate_top_trends(trend_data)
