from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from server.database import get_db
from server.services.recommender import train_and_store
from server.models.model_store import ModelStore
from pathlib import Path

router = APIRouter()

@router.post("/recommendation-engine", summary="Train and store recommendation model (NMF)", status_code=204)
def train_recommendation(db: Session = Depends(get_db)):
    path = train_and_store(db)
    if path is None:
        raise HTTPException(status_code=404, detail="No ratings data to train on")
    return Response(status_code=204)

@router.get("/recommendation-engine/status", summary="List stored recommendation models", response_model=None)
def recommendation_status(db: Session = Depends(get_db)):
    rows = db.query(ModelStore).order_by(ModelStore.created_at.desc()).limit(10).all()
    out = []
    for r in rows:
        out.append({"id": int(r.id), "path": str(r.path), "created_at": str(r.created_at)})
    return {"models": out}