import sys
import os
import pytest
from fastapi.testclient import TestClient

# Ensure backend directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import app as app_module
from app import app

# 1. Create a bulletproof mock model
class MockModel:
    def predict(self, x): 
        return [0]
    def predict_proba(self, x): 
        return [[0.85, 0.15]]

# 2. Force the app's global model variable to use our mock
app_module.model = MockModel()

# 3. Initialize the test client
client = TestClient(app)

def test_predict_success_flow():
    valid_payload = {
        "CreditScore": 700,
        "Age": 42,
        "Tenure": 3,
        "Balance": 25000.45,
        "NumOfProducts": 2,
        "HasCrCard": 1,
        "IsActiveMember": 1,
        "EstimatedSalary": 85000.00,
        "Geography_Germany": 0,
        "Geography_Spain": 1,
        "Gender_Male": 0
    }
    response = client.post("/predict", json=valid_payload)
    assert response.status_code == 200
    assert "churn_prediction" in response.json()
    assert "churn_probability" in response.json()

def test_predict_invalid_bounds():
    corrupted_payload = {
        "CreditScore": 650,
        "Age": 150,  # Fails Pydantic validation (le=100)
        "Tenure": 5,
        "Balance": 0.0,
        "NumOfProducts": 1,
        "HasCrCard": 1,
        "IsActiveMember": 1,
        "EstimatedSalary": 50000.0,
        "Geography_Germany": 0,
        "Geography_Spain": 0,
        "Gender_Male": 1
    }
    response = client.post("/predict", json=corrupted_payload)
    assert response.status_code == 422

def test_predict_geography_collision():
    clashing_payload = {
        "CreditScore": 600,
        "Age": 30,
        "Tenure": 4,
        "Balance": 12000.0,
        "NumOfProducts": 1,
        "HasCrCard": 1,
        "IsActiveMember": 0,
        "EstimatedSalary": 45000.0,
        "Geography_Germany": 1, # True
        "Geography_Spain": 1,   # True -> Collision trigger
        "Gender_Male": 1
    }
    response = client.post("/predict", json=clashing_payload)
    assert response.status_code == 422
    assert "Geography collision" in response.json()["detail"]
