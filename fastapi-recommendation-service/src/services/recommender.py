from sklearn.decomposition import NMF
import numpy as np
import os
import joblib
from datetime import datetime

class Recommender:
    def __init__(self, model_storage_path):
        self.model_storage_path = model_storage_path

    def train_model(self, user_item_matrix):
        model = NMF(n_components=10, init='random', random_state=0)
        model.fit(user_item_matrix)
        return model

    def save_model(self, model):
        version = self._get_new_version()
        model_filename = f"model_v{version}.joblib"
        model_path = os.path.join(self.model_storage_path, model_filename)
        joblib.dump(model, model_path)

    def _get_new_version(self):
        existing_models = [f for f in os.listdir(self.model_storage_path) if f.startswith("model_v")]
        versions = [int(f.split('_v')[1].split('.')[0]) for f in existing_models]
        return max(versions) + 1 if versions else 1

    def load_model(self, version):
        model_filename = f"model_v{version}.joblib"
        model_path = os.path.join(self.model_storage_path, model_filename)
        if os.path.exists(model_path):
            return joblib.load(model_path)
        else:
            raise FileNotFoundError(f"Model version {version} not found.")