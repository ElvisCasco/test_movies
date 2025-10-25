from fastapi import APIRouter, Request, Depends, Query, HTTPException, Path
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import or_, distinct, func
from server.database import get_db
from server.schemas.movies import MoviesListResponse, MovieAvgRating
from server.models.movies import MovieModel, GenreModel

router = APIRouter()

def _row_to_movie_dict(row: Dict[str, Any]) -> Dict[str, Any]:
    movie_id = int(row.get("movieId") or row.get("movie_id") or 0)
    title = row.get("title", "") or ""
    genres = row.get("genres", "")
    if isinstance(genres, str):
        genres_list = [g for g in genres.split("|") if g]
    elif isinstance(genres, list):
        genres_list = genres
    else:
        genres_list = []
    return {"movie_id": movie_id, "title": title, "genres": genres_list}

@router.get("/", response_model=MoviesListResponse, summary="List movies with pagination and optional search")
def list_movies(
    request: Request,
    limit: int = Query(10, ge=1),
    page: int = Query(1, ge=1),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    offset = (page - 1) * limit

    data = getattr(request.app.state, "data", None) or {}
    df = data.get("movies")
    if df is not None and hasattr(df, "empty") and not df.empty:
        if search:
            tokens = [t.strip() for t in str(search).split() if t.strip()]
            if tokens:
                import re
                pattern = "|".join(re.escape(t) for t in tokens)
                mask = df["title"].astype(str).str.contains(pattern, case=False, na=False, regex=True) | \
                       df["genres"].astype(str).str.contains(pattern, case=False, na=False, regex=True)
                df = df[mask]
        total = int(df.shape[0])
        rows = df.iloc[offset : offset + limit].to_dict(orient="records")
        movies = [_row_to_movie_dict(r) for r in rows]
        return {"movies": movies, "total": total, "page": page, "limit": limit}

    try:
        query = db.query(MovieModel).outerjoin(GenreModel)
    except Exception:
        raise HTTPException(status_code=503, detail="No data available")

    if search:
        tokens = [t.strip() for t in str(search).split() if t.strip()]
        if tokens:
            token_preds = []
            for t in tokens:
                token_preds.append(
                    or_(
                        MovieModel.title.ilike(f"%{t}%"),
                        GenreModel.genre_name.ilike(f"%{t}%")
                    )
                )
            from sqlalchemy import or_ as _or
            query = query.filter(_or(*token_preds))

    total = query.with_entities(distinct(MovieModel.movie_id)).count()
    results = query.distinct(MovieModel.movie_id).offset(offset).limit(limit).all()

    movies_out: List[Dict[str, Any]] = []
    for m in results:
        gnames = []
        if getattr(m, "genres", None):
            for g in m.genres:
                name = getattr(g, "genre_name", None)
                if name:
                    gnames.append(name)
        movies_out.append({"movie_id": m.movie_id, "title": m.title or "", "genres": gnames})

    return {"movies": movies_out, "total": total, "page": page, "limit": limit}


@router.get("/{movie_id}/avg-rating", response_model=MovieAvgRating, summary="Get average rating for a movie")
def movie_avg_rating(
    request: Request,
    movie_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    title = ""
    total = 0
    avg = 0.0
    data = getattr(request.app.state, "data", {}) or {}

    # find title from CSV if available
    movies_df = data.get("movies")
    if movies_df is not None and hasattr(movies_df, "empty") and not movies_df.empty:
        if "movieId" in movies_df.columns:
            mrows = movies_df[movies_df["movieId"] == movie_id]
        elif "movie_id" in movies_df.columns:
            mrows = movies_df[movies_df["movie_id"] == movie_id]
        else:
            mrows = movies_df.iloc[0:0]
        if not mrows.empty:
            title = str(mrows.iloc[0].get("title", "") or "")

    # CSV-first: compute avg/count from ratings CSV
    ratings_df = data.get("ratings")
    if ratings_df is not None and hasattr(ratings_df, "empty") and not ratings_df.empty:
        if "movieId" in ratings_df.columns:
            rrows = ratings_df[ratings_df["movieId"] == movie_id]
        elif "movie_id" in ratings_df.columns:
            rrows = ratings_df[ratings_df["movie_id"] == movie_id]
        else:
            rrows = ratings_df.iloc[0:0]
        total = int(rrows.shape[0])
        if total > 0:
            rating_col = "rating" if "rating" in rrows.columns else rrows.columns[0]
            try:
                avg = float(rrows[rating_col].astype(float).mean())
            except Exception:
                avg = 0.0
        return {"movie_id": movie_id, "title": title, "avg_rating": round(avg, 2), "total_ratings": total}

    # DB fallback: try import ratings model
    try:
        from server.models.ratings import RatingModel  # type: ignore
    except Exception:
        RatingModel = None

    if RatingModel is not None:
        agg = db.query(func.avg(RatingModel.rating), func.count(RatingModel.rating)).filter(RatingModel.movie_id == movie_id).one()
        avg_val, count_val = agg[0] or 0.0, int(agg[1] or 0)
        total = count_val
        avg = float(avg_val) if avg_val is not None else 0.0
        movie = db.query(MovieModel).filter(MovieModel.movie_id == movie_id).first()
        if movie:
            title = movie.title or ""
        return {"movie_id": movie_id, "title": title, "avg_rating": round(avg, 2), "total_ratings": total}

    raise HTTPException(status_code=404, detail="No ratings found for movie and no ratings data available")