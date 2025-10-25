import os

class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_STORAGE_PATH = os.path.join(BASE_DIR, 'artifacts', 'models')
    DATABASE_URL = "sqlite:///./database.db"  # Example database URL, adjust as needed
    API_V1_STR = "/api/rest/v1"