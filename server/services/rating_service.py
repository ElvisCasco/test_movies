from pydantic import BaseModel
from datetime import datetime
import pydantic as _pydantic

_pydantic_major = int(getattr(_pydantic, "__version__", "0").split(".")[0])

class RatingCreate(BaseModel):
    user_id: int
    movie_id: int
    rating: float

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