from pathlib import Path
import sys
import joblib
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts" / "models"

def find_latest_model(dirpath: Path):
    files = sorted(dirpath.glob("nmf_model_*.joblib"))
    return files[-1] if files else None

def top_n_for_user(model_path: Path, user_id: int, top_n: int = 10):
    data = joblib.load(model_path)
    W = data.get("W")
    H = data.get("H")
    user_ids = data.get("user_ids", [])
    movie_ids = data.get("movie_ids", [])

    if W is None or H is None:
        print("Model file missing W or H.")
        return

    try:
        idx = user_ids.index(user_id)
    except ValueError:
        print(f"user_id {user_id} not found in model user_ids")
        return

    scores = np.dot(W[idx], H)
    top_idx = np.argsort(-scores)[:top_n]
    results = [(int(movie_ids[i]), float(scores[i])) for i in top_idx]
    print(f"Top {top_n} recommendations for user {user_id}:")
    for mid, score in results:
        print(f"  movie_id={mid}  score={score:.4f}")

if __name__ == "__main__":
    if not ARTIFACTS_DIR.exists():
        print("No artifacts/models directory found. Train model first.")
        sys.exit(1)

    model_file = find_latest_model(ARTIFACTS_DIR)
    if model_file is None:
        print("No model files found in artifacts/models. Call POST /api/rest/v1/recommendation-engine first.")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: python get_recommendations.py <user_id> [top_n]")
        sys.exit(1)

    user = int(sys.argv[1])
    topn = int(sys.argv[2]) if len(sys.argv) >= 3 else 10
    top_n_for_user(model_file, user, topn)