from pydantic import BaseModel
from typing import List


class StrategicThemeInput(BaseModel):
    strategic_theme: str


class StrategicThemeResponse(BaseModel):
    theme_summary: str
    theme_recommendations: List[str]
