# main.py

from fastapi import FastAPI
from app.api.endpoints import strategic_theme2, trend_summary,swot_analysis,challenge_risk, vision, strategic_theme

app = FastAPI(
    title="Clarhet AI API",
    description="API for strategic business analysis, including Trends and SWOT.",
    version="1.0.0"
)
app.include_router(
    trend_summary.router, 
    prefix="/api/trends"
)
app.include_router(
    swot_analysis.router,
    prefix="/api/swot"
)

app.include_router(
    challenge_risk.router,
    prefix="/api/challenge"
)

app.include_router(
    vision.router,
    prefix="/api/blueprint"
)

app.include_router(
    strategic_theme.router,
    prefix="/api/blueprint"
    
)



#==============================
# Include the new strategic themes router
app.include_router(
    strategic_theme2.router,
    prefix="/api/strategic-theme2",
    tags=["Strategic Theme2"] # This creates a new section in the docs
)


@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to the Clarhet AI API. Visit /docs for the API documentation.",
        "available_endpoints": {
            "trends": "/api/trends/",
            "swot": "/api/swot/",
            "challenges": "/api/challenges/"
        }
    }