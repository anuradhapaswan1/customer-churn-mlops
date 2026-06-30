import os
from contextlib import asynccontextmanager
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.getenv("MODEL_PATH", os.path.join(BASE_DIR, "models", "churn_model.pkl"))

model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    try:
        model = joblib.load(MODEL_PATH) 
        print("[SUCCESS] Inference matrix elements successfully loaded into memory.")
    except Exception as e:
        print(f"[ERROR] Failed to load model at {MODEL_PATH}: {e}")
        raise e
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Added Field validation constraints so bad input triggers a 422 error automatically
class CustomerFeatures(BaseModel):
    CreditScore: int = Field(..., ge=300, le=850)
    Age: int = Field(..., ge=18, le=100) # Prevents Age: 150
    Tenure: int = Field(..., ge=0, le=10)
    Balance: float = Field(..., ge=0.0)
    NumOfProducts: int = Field(..., ge=1, le=4)
    HasCrCard: int = Field(..., ge=0, le=1)
    IsActiveMember: int = Field(..., ge=0, le=1)
    EstimatedSalary: float = Field(..., ge=0.0)
    Geography_Germany: int = Field(..., ge=0, le=1)
    Geography_Spain: int = Field(..., ge=0, le=1)
    Gender_Male: int = Field(..., ge=0, le=1)

@app.post("/predict")
def predict_churn(data: CustomerFeatures):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Custom business logic check: A customer cannot be in Germany and Spain at the same time
    if data.Geography_Germany == 1 and data.Geography_Spain == 1:
        raise HTTPException(status_code=422, detail="Geography collision: Customer cannot be in two regions simultaneously.")

    features = [[
        data.CreditScore,
        data.Age,
        data.Tenure,
        data.Balance,
        data.NumOfProducts,
        data.HasCrCard,
        data.IsActiveMember,
        data.EstimatedSalary,
        data.Geography_Germany,
        data.Geography_Spain,
        data.Gender_Male
    ]]
    
    prediction = int(model.predict(features)[0])
    probability = float(model.predict_proba(features)[0][1]) if hasattr(model, "predict_proba") else 0.0

    return {
        "churn_prediction": prediction,
        "churn_probability": probability
    }