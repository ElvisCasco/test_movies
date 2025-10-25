from fastapi import APIRouter, Request, HTTPException
from typing import List
from server.schemas.recommendations import RecommendedMoviesResponse, RecommendationItem
from server.services.recommendation_server import train_recommendation_model, user_recommendations

router = APIRouter()

@router.post("/train", response_model=dict)
def train(request: Request):
    data = getattr(request.app.state, "data", None)
    if not data:
        raise HTTPException(status_code=500, detail="No data loaded")
    model = train_recommendation_model(data)
    # optionally store model in app.state
    request.app.state.reco_model = model
    return {"status": "trained", "model_type": model.get("model_type")}

@router.get("/user/{user_id}", response_model=RecommendedMoviesResponse)
def recommend_user(user_id: int, request: Request, top_n: int = 10):
    data = getattr(request.app.state, "data", None)
    if not data:
        raise HTTPException(status_code=500, detail="No data loaded")
    recs = user_recommendations(user_id, data, top_n=top_n)
    items = [RecommendationItem(**r) for r in recs]
    return RecommendedMoviesResponse(user_id=user_id, recommendations=items)