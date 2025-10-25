from pydantic import BaseModel
from typing import List
import pydantic as _pydantic

_pydantic_major = int(getattr(_pydantic, "__version__", "0").split(".")[0])

class MovieOut(BaseModel):
    movie_id: int
    title: str
    genres: List[str] = []

    class Config:
        if _pydantic_major >= 2:
            from_attributes = True
        else:
            orm_mode = True

class MoviesListResponse(BaseModel):
    movies: List[MovieOut] = []
    total: int
    page: int
    limit: int

class MovieAvgRating(BaseModel):
    movie_id: int
    title: str
    avg_rating: float
    total_ratings: int

    class Config:
        if _pydantic_major >= 2:
            from_attributes = True
        else:
            orm_mode = True