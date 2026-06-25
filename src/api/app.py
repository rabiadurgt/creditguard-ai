from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import pandas as pd

from src.pipeline.feature_pipeline import FeaturePipeline
from src.explainability.shap_explainer import SHAPExplainer

app = FastAPI(title="CreditGuard AI API")


# -------------------------
# LOAD MODEL + FEATURES
# -------------------------
MODEL_PATH = "artifacts/models/lgbm_optuna_cv.pkl"
FEATURE_PATH = "artifacts/features/final_features.pkl"

model = joblib.load(MODEL_PATH)
MODEL_FEATURES = joblib.load(FEATURE_PATH)

# SHAP background 
background_df = pd.DataFrame([dict.fromkeys(MODEL_FEATURES, 0)])
explainer = SHAPExplainer(model, background_df)

pipeline = FeaturePipeline()


# -------------------------
# INPUT SCHEMA
# -------------------------
class CreditRequest(BaseModel):

    AMT_CREDIT: float = Field(example=100000)
    AMT_ANNUITY: float = Field(example=5000)
    AMT_INCOME_TOTAL: float = Field(example=120000)
    DAYS_BIRTH: float = Field(example=-12000)
    DAYS_EMPLOYED: float = Field(example=-3000)

    CNT_FAM_MEMBERS: float = Field(example=2)
    CNT_CHILDREN: float = Field(example=1)

    FLAG_OWN_CAR: str = Field(example="Y")
    FLAG_OWN_REALTY: str = Field(example="N")


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

    # 1. raw input
    df = pd.DataFrame([request.model_dump()])

    # 2. feature pipeline
    df = pipeline.transform_application(df)

    # 3. preprocessing safety layer
    from src.preprocessing.missing_handler import handle_missing_values
    from src.preprocessing.encoder import encode_categorical_features

    df = handle_missing_values(df)
    df = encode_categorical_features(df)

    # 4. align with training features
    X = df.reindex(columns=MODEL_FEATURES, fill_value=0)

    # 5. prediction
    probability = model.predict_proba(X)[:, 1][0]

    # 6. risk level
    risk_level = (
        "HIGH" if probability > 0.70
        else "MEDIUM" if probability > 0.30
        else "LOW"
    )

    # 7. SHAP EXPLANATION (NEW)
    explanations = explainer.explain(X, top_k=5)

    return {
        "risk_score": float(probability),
        "risk_level": risk_level,
        "explanations": explanations
    }