from fastapi import APIRouter, Body, HTTPException
from app.api.models.strategic_theme_model import StrategicThemeInput, StrategicThemeResponse
from app.services.strategic_theme_service import process_strategic_theme

router = APIRouter()

@router.post("/analyze/strategic_theme", response_model=StrategicThemeResponse, tags= ["Strategic Theme"])


async def analyze_strategic_theme_endpoint(data: StrategicThemeInput= Body(..., example={
    
    "strategic_theme": "Focus on sustainability and innovation in technology solutions."
    })):
    """_summary_

    Args:
        data (_type_, optional): _description_. Defaults to Body(..., example={  "strategic_theme": "Focus on sustainability and innovation in technology solutions." }).
    """
    try:
        return await process_strategic_theme(data.strategic_theme)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"strategic theme processing failed: {str(e)}")
