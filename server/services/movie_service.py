from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import or_, distinct

from server.models.movies import MovieModel, GenreModel


def get_movie(db: Session, movie_id: int):
    return db.query(MovieModel).filter(MovieModel.movie_id == movie_id).first()


def get_movies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MovieModel).offset(skip).limit(limit).all()


def list_movies(db: Session, limit: int = 10, page: int = 1, search: Optional[str] = None) -> Dict[str, Any]:
    """
    Return paginated list of movies with optional search across Movie.title and Genre.genre_name.

    Response format:
    {
        "movies": [...],
        "total": <int>,
        "page": <int>,
        "limit": <int>
    }
    """
    offset = (page - 1) * limit
    query = db.query(MovieModel).outerjoin(GenreModel)

    if search:
        tokens = [t.strip() for t in str(search).split() if t.strip()]
        if tokens:
            preds: List = []
            for t in tokens:
                preds.append(
                    or_(
                        MovieModel.title.ilike(f"%{t}%"),
                        GenreModel.genre_name.ilike(f"%{t}%"),
                    )
                )
            query = query.filter(or_(*preds))

    total = query.with_entities(distinct(MovieModel.movie_id)).count()
    results = query.distinct(MovieModel.movie_id).offset(offset).limit(limit).all()

    movies_out: List[Dict[str, Any]] = []
    for m in results:
        gnames: List[str] = []
        for g in getattr(m, "genres", []) or []:
            name = getattr(g, "genre_name", None)
            if name:
                gnames.append(name)
        movies_out.append({"movie_id": m.movie_id, "title": m.title or "", "genres": gnames})

    return {"movies": movies_out, "total": total, "page": page, "limit": limit}