import pandas as pd
from typing import Dict, List, Any

def train_recommendation_model(data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    ratings = data.get("ratings")
    movies = data.get("movies")

    if ratings is None or ratings.empty:
        return {"model_type": "popularity", "scores": pd.DataFrame()}

    agg = ratings.groupby("movieId")["rating"].agg(["mean", "count"]).reset_index()
    agg = agg.rename(columns={"mean": "avg_rating", "count": "rating_count"})
    if movies is not None and not movies.empty and "movieId" in movies.columns:
        agg = agg.merge(movies[["movieId", "title"]], on="movieId", how="left")
    agg = agg.sort_values(["avg_rating", "rating_count"], ascending=[False, False])
    return {"model_type": "popularity", "scores": agg}

def user_recommendations(user_id: int, data: Dict[str, pd.DataFrame], top_n: int = 10) -> List[Dict[str, Any]]:
    ratings = data.get("ratings")
    movies = data.get("movies")

    if ratings is None or ratings.empty:
        return []

    user_rated = set(ratings[ratings["userId"] == user_id]["movieId"].unique())

    agg = ratings.groupby("movieId")["rating"].agg(["mean", "count"]).reset_index()
    agg = agg.rename(columns={"mean": "avg_rating", "count": "rating_count"})
    candidates = agg[~agg["movieId"].isin(user_rated)]
    candidates = candidates.sort_values(["avg_rating", "rating_count"], ascending=[False, False])
    top = candidates.head(top_n)

    results = []
    for _, row in top.iterrows():
        movie_id = int(row["movieId"])
        title = None
        if movies is not None and not movies.empty and "movieId" in movies.columns:
            m = movies[movies["movieId"] == movie_id]
            if not m.empty:
                title = m.iloc[0].get("title")
        results.append({
            "movie_id": movie_id,
            "title": title,
            "avg_rating": float(row["avg_rating"]),
            "rating_count": int(row["rating_count"])
        })
    return results

__all__ = ["train_recommendation_model", "user_recommendations"]