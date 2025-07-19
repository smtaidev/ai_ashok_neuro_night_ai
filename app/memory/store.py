# # Step 1: Create memory/store.py for shared input storage

# # app/memory/store.py
# from typing import Optional
# from app.api.models.trend_summary_model import TrendDataInput

# # Shared in-memory storage (replaced every time /summary is called)
# last_trend_input: Optional[TrendDataInput] = None


# app/memory/store.py

from typing import Optional
from app.api.models.trend_summary_model import TrendDataInput
from app.api.models.swot_model import SWOTDataInput

# Shared in-memory storage
# last_trend_input: Optional[TrendDataInput] = None
last_swot_input: Optional[SWOTDataInput] = None