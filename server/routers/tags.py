from fastapi import APIRouter, Request, HTTPException
from typing import List, Dict

router = APIRouter()

@router.get("/", response_model=List[Dict])
def list_tags(request: Request, limit: int = 100):
    df = request.app.state.data.get("tags")
    if df is None:
        raise HTTPException(status_code=500, detail="Tags data not loaded")
    records = df.head(limit).to_dict(orient="records")
    return records