from pydantic import BaseModel
from typing import List

class RecommendationRequest(BaseModel):
    user_id: int
    item_ids: List[int]

class RecommendationResponse(BaseModel):
    recommended_items: List[int]
    model_version: str