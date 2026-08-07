from urllib import response

from fastapi import FastAPI
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
import joblib
import pandas as pd
import time

from src.pipeline.feature_pipeline import FeaturePipeline
from src.explainability.shap_explainer import SHAPExplainer
from src.rag.rag_service import RAGService
from src.agent.agent import CreditAgent
from src.utils.logger import log_prediction

# -------------------------
# GLOBAL STATE
# -------------------------
rag = None
explainer = None
pipeline = None
model = None
MODEL_FEATURES = None
agent = None


# -------------------------
# LIFESPAN
# -------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):

    global rag, explainer, pipeline, model, MODEL_FEATURES, agent

    MODEL_PATH = "artifacts/models/lgbm_optuna_cv.pkl"
    FEATURE_PATH = "artifacts/features/final_features.pkl"

    # -------------------------
    # LOAD MODEL
    # -------------------------
    model = joblib.load(MODEL_PATH)
    MODEL_FEATURES = joblib.load(FEATURE_PATH)

    if MODEL_FEATURES is None:
        raise RuntimeError("MODEL_FEATURES not loaded")

    print("MODEL FEATURES:")
    print(MODEL_FEATURES)

    # -------------------------
    # PIPELINE
    # -------------------------
    pipeline = FeaturePipeline()

    # -------------------------
    # RAG
    # -------------------------
    rag = RAGService()

    # -------------------------
    # SHAP
    # -------------------------
    background_df = pd.DataFrame([dict.fromkeys(MODEL_FEATURES, 0)])
    explainer = SHAPExplainer(model, background_df)

    # -------------------------
    # AGENT
    # -------------------------
    agent = CreditAgent(
        rag_service=rag,
        explainer=explainer,
        model=model
    )

    print("🚀 CreditGuard AI initialized")

    yield

    print("🛑 System shutdown")


# -------------------------
# FASTAPI APP
# -------------------------
app = FastAPI(
    title="CreditGuard AI API",
    lifespan=lifespan
)


# -------------------------
# REQUEST SCHEMA
# -------------------------
class CreditRequest(BaseModel):

    # ==========================
    # Financial
    # ==========================

    AMT_CREDIT: float = Field(example=100000)

    AMT_ANNUITY: float = Field(example=5000)

    AMT_INCOME_TOTAL: float = Field(example=120000)

    AMT_GOODS_PRICE: float = Field(
        default=0,
        example=80000
    )


    # ==========================
    # External Scores
    # ==========================

    EXT_SOURCE_1: float = Field(
        default=0.5,
        example=0.75
    )

    EXT_SOURCE_2: float = Field(
        default=0.5,
        example=0.80
    )

    EXT_SOURCE_3: float = Field(
        default=0.5,
        example=0.75
    )


    # ==========================
    # Personal
    # ==========================

    DAYS_BIRTH: float = Field(
        example=-15000
    )

    DAYS_EMPLOYED: float = Field(
        example=-5000
    )


    CNT_FAM_MEMBERS: float = Field(
        example=3
    )

    CNT_CHILDREN: float = Field(
        example=1
    )


    CODE_GENDER: str = Field(
        default="M",
        example="F"
    )


    # ==========================
    # Assets
    # ==========================

    FLAG_OWN_CAR: str = Field(
        example="Y"
    )

    FLAG_OWN_REALTY: str = Field(
        example="Y"
    )


    # ==========================
    # Engineered Features
    # ==========================

    annuity_credit_ratio: float = Field(
        default=0
    )

    active_contracts: float = Field(
        default=0
    )

    late_payment_ratio: float = Field(
        default=0
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

    start_time = time.perf_counter()

    raw_request = request.model_dump()

    # 1. dataframe
    df = pd.DataFrame([raw_request])

    # 2. feature engineering
    df = pipeline.transform_application(df)

    print("\n====== AFTER PIPELINE ======")
    print(df.columns.tolist())


    print("\n====== IMPORTANT FEATURES ======")

    for col in [
        "EXT_SOURCE_1",
        "EXT_SOURCE_2",
        "EXT_SOURCE_3",
        "AMT_GOODS_PRICE",
        "CODE_GENDER",
        "annuity_credit_ratio"
    ]:
        if col in df.columns:
            print(col, "=", df[col].iloc[0])
        else:
            print(col, "MISSING")
    

    # 4. align features
    X = df.reindex(columns=MODEL_FEATURES, fill_value=0)

    # 5. prediction
    probability = float(model.predict_proba(X)[:, 1][0])

    # 6. agent reasoning
    agent_result = agent.run(
        raw_request,
        X,
        probability
    )

    response_time_ms = (
        time.perf_counter() - start_time
    ) * 1000

    # ===============================
    # DEBUG
    # ===============================

    print("\n========== DECISION DEBUG ==========")
    print(f"Model Score     : {probability:.4f}")
    print(f"Business Score  : {agent_result['audit']['business_score']:.4f}")
    print(f"Policy Score    : {agent_result['audit']['policy_score']:.4f}")
    print(f"Final Score     : {agent_result['audit']['final_score']:.4f}")
    print(f"Decision        : {agent_result['decision']['status']}")
    print("====================================\n")

    response = {
        "risk_score": probability,
        "risk_level": agent_result["risk_level"],
        "decision": agent_result["decision"],
        "confidence": agent_result["confidence"],
        "response_time_ms": round(response_time_ms, 2),
        
        "triggered_rules": agent_result["triggered_rules"],
        "matched_policies": agent_result["matched_policies"],
        "audit": agent_result["audit"],

        "explanations": agent_result["explanations"],
        "policies": agent_result["policies"],

        "meta": {
            "model": "LightGBM + Optuna",
            "rag": "FAISS + MiniLM",
            "agent": "Hybrid Credit Decision Agent",
            "version": "2.0.0"
        }
    }

    # ----------------------------------------
    # Save prediction log
    # ----------------------------------------

    log_prediction(
        raw_request,
        response
    )

    return response

# -------------------------
# POLICY + RAG ENDPOINT
# -------------------------
@app.post("/policy-explain")
def explain_policy(request: CreditRequest):

    df = pd.DataFrame([request.model_dump()])

    # pipeline
    df = pipeline.transform_application(df)
    df = pipeline.preprocess(df)

    X = df.reindex(columns=MODEL_FEATURES, fill_value=0)

    prob = model.predict_proba(X)[:, 1][0]

    # strong semantic query (RAG optimized)
    query = (
        f"Credit risk assessment: "
        f"income {df['AMT_INCOME_TOTAL'].values[0]}, "
        f"credit {df['AMT_CREDIT'].values[0]}, "
        f"employment {df['DAYS_EMPLOYED'].values[0]}"
    )

    explanations = rag.explain(query)

    return {
        "risk_score": float(prob),
        "explanations": explanations,
        "meta": {
            "retrieval": "RAG-policy-system"
        }
    }

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }
