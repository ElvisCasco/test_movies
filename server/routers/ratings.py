from fastapi import APIRouter, Depends, HTTPException, Request, Query
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from typing import Optional

from server.database import get_db, engine
from server.models.ratings import RatingModel
from server.models.movies import MovieModel
from server.schemas.ratings import RatingCreate, RatingOut

router = APIRouter()

class MovieRatingResponse(BaseModel):
    movie_id: int
    avg_rating: Optional[float] = None
    count: int = 0

#@router.get("/{movie_id}/avg-rating", response_model=MovieRatingResponse)
#def avg_rating(movie_id: int, request: Request, db: Session = Depends(get_db)):
#    # Try CSV in memory first
#    data = getattr(request.app.state, "data", None)
#    if data and "ratings" in data and not data["ratings"].empty:
#        df = data["ratings"]
#        matches = df[df["movieId"] == movie_id]
#        count = int(matches.shape[0])
#        if count == 0:
#            return MovieRatingResponse(movie_id=movie_id, avg_rating=None, count=0)
#        avg = float(matches["rating"].mean())
#        return MovieRatingResponse(movie_id=movie_id, avg_rating=avg, count=count)

#    # Fallback to DB model
#    try:
#        from server.models.ratings import RatingModel
#    except Exception:
#        raise HTTPException(status_code=500, detail="No ratings CSV loaded and DB model unavailable")

#    rows = db.query(RatingModel).filter(RatingModel.movie_id == movie_id).all()
#    if not rows:
#        return MovieRatingResponse(movie_id=movie_id, avg_rating=None, count=0)
#    count = len(rows)
#    avg = sum(r.rating for r in rows) / count
#    return MovieRatingResponse(movie_id=movie_id, avg_rating=avg, count=count)


@router.post("/", response_model=None, summary="Create a rating")
def create_rating(payload: RatingCreate, db: Session = Depends(get_db)):
    RatingModel.__table__.create(bind=engine, checkfirst=True)

    if not (0.5 <= float(payload.rating) <= 5.0):
        raise HTTPException(status_code=400, detail="rating must be between 0.5 and 5.0")

    try:
        movie_exists = db.query(MovieModel).filter(MovieModel.movie_id == payload.movie_id).first() is not None
    except Exception:
        movie_exists = True

    if not movie_exists:
        raise HTTPException(status_code=404, detail="movie not found")

    rating = RatingModel(user_id=payload.user_id, movie_id=payload.movie_id, rating=payload.rating)
    db.add(rating)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="rating for this user/movie already exists or constraint violated")
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(exc))
    db.refresh(rating)

    return {
        "rating_id": int(rating.rating_id),
        "user_id": int(rating.user_id),
        "movie_id": int(rating.movie_id),
        "rating": float(rating.rating),
        "timestamp": rating.timestamp.isoformat() if getattr(rating, "timestamp", None) else datetime.utcnow().isoformat(),
    }

@router.get("/", response_model=None, summary="List ratings with optional filters")
def list_ratings(
    request: Request,
    limit: int = Query(100, ge=1),
    page: int = Query(1, ge=1),
    movie_id: Optional[int] = Query(None),
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    offset = (page - 1) * limit
    data = getattr(request.app.state, "data", {}) or {}
    df = data.get("ratings")
    if df is not None and hasattr(df, "empty") and not df.empty:
        q = df
        if movie_id is not None:
            if "movieId" in q.columns:
                q = q[q["movieId"] == movie_id]
            elif "movie_id" in q.columns:
                q = q[q["movie_id"] == movie_id]
            else:
                q = q.iloc[0:0]
        if user_id is not None:
            if "userId" in q.columns:
                q = q[q["userId"] == user_id]
            elif "user_id" in q.columns:
                q = q[q["user_id"] == user_id]
            else:
                q = q.iloc[0:0]
        total = int(q.shape[0])
        rows = q.iloc[offset : offset + limit].to_dict(orient="records")
        return {"ratings": rows, "total": total, "page": page, "limit": limit}

    query = db.query(RatingModel)
    if movie_id is not None:
        query = query.filter(RatingModel.movie_id == movie_id)
    if user_id is not None:
        query = query.filter(RatingModel.user_id == user_id)

    total = query.count()
    results = query.offset(offset).limit(limit).all()

    out: List[Dict[str, Any]] = []
    for r in results:
        out.append({
            "rating_id": int(r.rating_id),
            "user_id": int(r.user_id),
            "movie_id": int(r.movie_id),
            "rating": float(r.rating),
            "timestamp": r.timestamp.isoformat() if getattr(r, "timestamp", None) else None,
        })

    return {"ratings": out, "total": total, "page": page, "limit": limit}