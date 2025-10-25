import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_train_recommendation_model():
    response = client.post("/api/rest/v1/recommendation-engine", json={
        "user_id": 1,
        "movie_id": 1,
        "rating": 4.5
    })
    assert response.status_code == 200
    assert "model_version" in response.json()

def test_train_recommendation_model_invalid_data():
    response = client.post("/api/rest/v1/recommendation-engine", json={
        "user_id": "invalid_id",
        "movie_id": 1,
        "rating": 4.5
    })
    assert response.status_code == 422

def test_model_storage():
    response = client.post("/api/rest/v1/recommendation-engine", json={
        "user_id": 1,
        "movie_id": 2,
        "rating": 5.0
    })
    model_version = response.json()["model_version"]
    
    # Check if the model is stored correctly
    model_path = f"artifacts/models/model_v{model_version}.joblib"
    assert os.path.exists(model_path)  # Ensure the model file exists

    # Clean up the model file after test
    os.remove(model_path)  # Remove the model file after the test