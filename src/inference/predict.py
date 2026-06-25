import joblib
import pandas as pd

from src.preprocessing.prepare_dataset import prepare_dataset
from src.feature_store.final_features import FINAL_FEATURES

MODEL_PATH = "artifacts/models/lgbm_optuna_cv.pkl"


def load_model():
    return joblib.load(MODEL_PATH)


def predict(input_path: str):

    print("Loading data...")

    df = prepare_dataset(input_path)

    print("Raw shape:", df.shape)

    # -------------------------
    # ID saklama (opsiyonel)
    # -------------------------
    if "SK_ID_CURR" in df.columns:
        ids = df["SK_ID_CURR"]
        df = df.drop(columns=["SK_ID_CURR"])
    else:
        ids = None

    # -------------------------
    # FEATURE SELECTION
    # -------------------------
    X = df[[c for c in FINAL_FEATURES if c in df.columns]]

    print("After feature selection:", X.shape)

    # -------------------------
    # LOAD MODEL
    # -------------------------
    model = load_model()

    # -------------------------
    # PREDICT
    # -------------------------
    preds = model.predict_proba(X)[:, 1]

    result = pd.DataFrame({
        "SK_ID_CURR": ids,
        "default_probability": preds
    })

    print("Inference completed.")

    return result


if __name__ == "__main__":

    output = predict("data/processed/train_feature_store.parquet")
    print(output.head())