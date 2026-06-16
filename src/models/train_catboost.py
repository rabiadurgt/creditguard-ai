import joblib

from catboost import CatBoostClassifier

from src.preprocessing.prepare_dataset import (
    prepare_dataset
)

from src.preprocessing.splitter import (
    split_dataset
)


def train_catboost():

    print("Preparing dataset...")

    df = prepare_dataset(
        "data/processed/train_feature_store.parquet"
    )

    print(df.shape)

    X_train, X_valid, y_train, y_valid = (
        split_dataset(df)
    )

    print(
        f"Train shape: {X_train.shape}"
    )

    print(
        f"Validation shape: {X_valid.shape}"
    )

    model = CatBoostClassifier(
        iterations=1000,
        learning_rate=0.05,
        depth=6,
        loss_function="Logloss",
        eval_metric="AUC",
        random_seed=42,
        verbose=100
    )

    print("Training CatBoost...")

    model.fit(
        X_train,
        y_train
    )

    joblib.dump(
        model,
        "artifacts/models/catboost_baseline.pkl"
    )

    print("Model saved.")

    return (
        model,
        X_valid,
        y_valid
    )