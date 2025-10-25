from pathlib import Path
from typing import Dict
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FOLDER = PROJECT_ROOT / "data" / "small"

CSV_FILES = {
    "movies": "movies.csv",
    "ratings": "ratings.csv",
    "tags": "tags.csv",
}

def load_csvs() -> Dict[str, pd.DataFrame]:
    data = {}
    for key, fname in CSV_FILES.items():
        path = DATA_FOLDER / fname
        if path.exists():
            try:
                df = pd.read_csv(path)
            except Exception as e:
                print(f"Failed to read {path}: {e}")
                df = pd.DataFrame()
            # normalize common column names
            if "movieId" not in df.columns and "movie_id" in df.columns:
                df = df.rename(columns={"movie_id": "movieId"})
            if "userId" not in df.columns and "user_id" in df.columns:
                df = df.rename(columns={"user_id": "userId"})
            if key == "movies" and "genres" not in df.columns:
                df["genres"] = ""
            data[key] = df
        else:
            data[key] = pd.DataFrame()
    return data