from pathlib import Path
import joblib
import os

MODEL_DIR = Path(__file__).resolve().parent.parent / 'artifacts/models'

def save_model(model, version):
    model_path = MODEL_DIR / f'model_v{version}.joblib'
    joblib.dump(model, model_path)

def get_latest_version():
    versions = [int(f.stem.split('_v')[-1]) for f in MODEL_DIR.glob('model_v*.joblib')]
    return max(versions) + 1 if versions else 1

def store_model(model):
    version = get_latest_version()
    save_model(model, version)