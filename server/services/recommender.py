from pathlib import Path
from datetime import datetime
from joblib import dump
import pandas as pd
from sklearn.decomposition import NMF
from sqlalchemy.orm import Session

from server.models.ratings import RatingModel
from server.models.model_store import ModelStore

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts" / "models"

def train_and_store(db: Session, n_components: int = 20) -> str | None:
    rows = db.query(RatingModel.user_id, RatingModel.movie_id, RatingModel.rating).all()
    if not rows:
        return None

    df = pd.DataFrame(rows, columns=["user_id", "movie_id", "rating"])
    mat = df.pivot_table(index="user_id", columns="movie_id", values="rating", fill_value=0)

    user_ids = mat.index.to_list()
    movie_ids = mat.columns.to_list()
    X = mat.values

    min_dim = min(X.shape)
    n_comp = max(1, min(n_components, min_dim - 1 if min_dim > 1 else 1))

    model = NMF(n_components=n_comp, init="random", random_state=0, max_iter=200)
    W = model.fit_transform(X)
    H = model.components_

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    fname = ARTIFACTS_DIR / f"nmf_model_{ts}.joblib"
    dump({
        "model": model,
        "W": W,
        "H": H,
        "user_ids": user_ids,
        "movie_ids": movie_ids,
        "trained_at": datetime.utcnow().isoformat(),
    }, str(fname))

    ms = ModelStore(path=str(fname), created_at=datetime.utcnow())
    db.add(ms)
    db.commit()

    return str(fname)