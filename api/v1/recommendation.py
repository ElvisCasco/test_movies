from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.recommender import train_model
import os

router = APIRouter()

class TrainingData(BaseModel):
    user_id: int
    movie_id: int
    rating: float

@router.post("/api/rest/v1/recommendation-engine")
async def create_recommendation_model(data: list[TrainingData]):
    try:
        model_version = train_model(data)
        return {"message": "Model trained successfully", "model_version": model_version}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))