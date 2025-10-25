from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import pydantic as _pydantic

_pydantic_major = int(getattr(_pydantic, "__version__", "0").split(".")[0])

class RatingCreateRequest(BaseModel):
    user_id: int
    movie_id: int
    rating: float
    review: Optional[str] = None

class RatingResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: float
    review: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class RatingCreate(BaseModel):
    user_id: int
    movie_id: int
    rating: float
    review: Optional[str] = None

class RatingOut(BaseModel):
    rating_id: int
    user_id: int
    movie_id: int
    rating: float
    timestamp: datetime

    class Config:
        if _pydantic_major >= 2:
            from_attributes = True
        else:
            orm_mode = True