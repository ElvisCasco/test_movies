from pydantic import BaseModel
from typing import Optional, List

class RecommendationItem(BaseModel):
    movie_id: int
    title: Optional[str] = None
    avg_rating: Optional[float] = None
    rating_count: Optional[int] = 0

class RecommendedMoviesResponse(BaseModel):
    user_id: int
    recommendations: List[RecommendationItem] = []