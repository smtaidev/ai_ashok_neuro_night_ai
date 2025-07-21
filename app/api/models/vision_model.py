# app/api/models/vision_model.py

from pydantic import BaseModel, Field
from typing import List, Optional

class VisionInput(BaseModel):
    
    """
    Input model for vision endpoint.
    
    Attributes:
        vision_statement (str): A text describing the user's business vision.
    """
    
    vision_statement: str
    
    
class VisionResponse(BaseModel):
    
    
    """
    Response model for processed vision analysis.
    
    Attributes:
        vision_score (int): A score between 1 to 100 evaluating the quality and clarity of the vision.
        vision_summary (str): A concise summary of the vision statement.
        vision_recommendations (List[str]): Suggestions to improve the clarity, focus, or ambition of the vision.
        vision_alt (List[str]): Three AI-generated alternative versions of the vision statement.
    """

    
    
    vision_score: int = Field(..., ge=0, le=100) # Score from 1 to 100
    vision_summary: str = Field(..., examples = ["A clear and ambitious vision for the future of the business."])
    vision_recommendations: List[str] = Field(..., 
                                              examples=[
                                                    "Consider making the vision more specific to your target market.",
                                                    "Ensure the vision aligns with current industry trends.",
                                                    "Focus on long-term goals and sustainability."
                                              ]
                                              
                                              )
    vision_alt : List[str] = Field(..., 
                                   min_length=3, 
                                   max_length=3,
                                   examples= [
                                        "To revolutionize the way businesses interact with technology.",
                                        "Empowering businesses to achieve their full potential through innovative solutions.",
                                        "Leading the industry in sustainable and ethical business practices."
                                   ])

    