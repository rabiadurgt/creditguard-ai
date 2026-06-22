from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import pandas as pd

from src.feature_store.final_features import FINAL_FEATURES

app = FastAPI(title="CreditGuard AI API")

# -------------------------
# MODEL LOAD
# -------------------------
MODEL_PATH = "artifacts/models/lgbm_optuna_cv.pkl"
model = joblib.load(MODEL_PATH)


# -------------------------
# INPUT SCHEMA
# -------------------------
class CreditRequest(BaseModel):
    features: dict = Field(
        example={
            "EXT_SOURCE_3": 0.5,
            "AMT_CREDIT": 100000,
            "DAYS_BIRTH": -12000
        }
    )


# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/")
def health():
    return {
        "status": "ok",
        "message": "CreditGuard AI is running"
    }


# -------------------------
# PREDICT ENDPOINT
# -------------------------
@app.post("/predict")
def predict(request: CreditRequest):

    # 1. JSON → DataFrame
    df = pd.DataFrame([request.features])

    # 2. Feature alignment (CRITICAL)
    X = df.reindex(columns=FINAL_FEATURES, fill_value=0)

    # 3. Prediction
    prob = model.predict_proba(X)[:, 1][0]

    # 4. Response
    return {
        "risk_score": float(prob),
        "risk_level": (
            "HIGH" if prob > 0.7 else
            "MEDIUM" if prob > 0.3 else
            "LOW"
        )
    }