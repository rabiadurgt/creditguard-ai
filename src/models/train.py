import joblib
import lightgbm as lgb

from src.preprocessing.prepare_dataset import prepare_dataset
from src.preprocessing.splitter import split_dataset
from src.feature_store.final_features import FINAL_FEATURES


def train_model():

    print("Preparing dataset...")

    df = prepare_dataset(
        "data/processed/train_feature_store.parquet"
    )

    print("Full dataset shape:", df.shape)

    # -------------------------
    # TARGET SPLIT
    # -------------------------
    X = df.drop(columns=["TARGET"])
    y = df["TARGET"]

    # -------------------------
    # FEATURE FREEZE
    # -------------------------
    X = X[[c for c in FINAL_FEATURES if c in X.columns]]

    print("After feature selection shape:", X.shape)

    # -------------------------
    # TRAIN / VALID SPLIT
    # -------------------------
    X_train, X_valid, y_train, y_valid = split_dataset(X, y)

    print(f"Train shape: {X_train.shape}")
    print(f"Validation shape: {X_valid.shape}")

    # -------------------------
    # MODEL
    # -------------------------
    model = lgb.LGBMClassifier(

        n_estimators=1362,
        learning_rate=0.09460095501084868,
        num_leaves=87,
        max_depth=3,
        min_child_samples=121,
        subsample=0.7829257002191399,
        colsample_bytree=0.6053061501418525,
        reg_alpha=4.147506457250209,
        reg_lambda=2.240416755904384,
        random_state=42,
        n_jobs=-1,
        verbosity=-1
    )

    print("Training model...")

    model.fit(
        X_train,
        y_train
    )

    # -------------------------
    # SAVE MODEL
    # -------------------------
    joblib.dump(
        model,
        "artifacts/models/lgbm_optuna_cv.pkl"
    )

    print("Model saved.")

    return model, X_valid, y_valid