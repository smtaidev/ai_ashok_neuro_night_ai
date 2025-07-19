from pydantic import BaseModel
from typing import List


class TopTrendsResponse(BaseModel):
    top_trends: List[str]  
    