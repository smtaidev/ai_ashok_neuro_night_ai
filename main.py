# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import strategic_theme2, trend_summary,swot_analysis,challenge_risk, vision, differentiation, chat_api, business_goal2 

app = FastAPI(
    title="Zenith AI API",
    description="API for strategic business analysis, including Trends and SWOT.",
    version="1.2.1"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

# trend_summary route:
app.include_router(
    trend_summary.router, 
    prefix="/api/trends"
)

# swot_analysis route:
app.include_router(
    swot_analysis.router,
    prefix="/api/swot"
)

# challenge_risk route:
app.include_router(
    challenge_risk.router,
    prefix="/api/challenge"
)

# vision route:
app.include_router(
    vision.router,
    prefix="/api/blueprint"
)

# strategic_theme2 route:
app.include_router(
    strategic_theme2.router,
    prefix="/api/strategic-theme2",
    tags=["Strategic Theme2"] 
)

# differentiation route:
app.include_router(
    differentiation.router,
    prefix="/api/differentiation",
    tags=["Differentiation Analysis"]
)

# business_goal2 route:
app.include_router(
    business_goal2.router,
    prefix="/api/business-goal",
    tags=["Business Goals"] 
)

# chat_api route:
app.include_router(
    chat_api.router,
    prefix="/api/chatbot",
    tags=["Chatbot"]
)

# Root endpoint:
@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to the Zenith AI API. Visit /docs for the API documentation.",
        "available_endpoints": {
            
            "trends_analysis": "/api/trends/analyze",
            "swot_analysis": "/api/swot/analysis",
            "challenge_risk_evaluate": "/api/challenge/evaluate",
            "challenge_risk_recommendations": "/api/challenge/recommendations",
            "vision_analysis": "/api/blueprint/vision",
            "strategic_theme2_combined": "/api/strategic-theme2/combined-analysis",
            "differentiation_analysis": "/api/differentiation/analyze",
            "business_goal_analysis": "/api/business-goal/analyze2",
            "chatbot": "/api/chatbot/chatbot"
            
        }
    }
