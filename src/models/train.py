import joblib
import lightgbm as lgb

from src.preprocessing.prepare_dataset import (
    prepare_dataset
)

from src.preprocessing.splitter import (
    split_dataset
)

def train_model():

    print("Preparing dataset...")

    df = prepare_dataset(
        "data/processed/train_feature_store.parquet"
    )

    print(df.shape)

    X_train, X_valid, y_train, y_valid = split_dataset(
        df
    )

    print(
        f"Train shape: {X_train.shape}"
    )

    print(
        f"Validation shape: {X_valid.shape}"
    )

    model = lgb.LGBMClassifier(
        n_estimators=878,
        learning_rate=0.06267844215476331,
        num_leaves=147,
        max_depth=5,
        min_child_samples=139,
        subsample=0.8117252089171065,
        colsample_bytree=0.8787079632913819,
        objective="binary",
        metric="auc",
        verbosity=-1,
        random_state=42,
        n_jobs=-1
    )

    print("Training model...")

    model.fit(
        X_train,
        y_train
    )

    joblib.dump(
        model,
        "artifacts/models/lgbm_tuned.pkl"
    )

    print("Model saved.")

    return (
        model,
        X_valid,
        y_valid
    )