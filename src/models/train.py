import joblib
import lightgbm as lgb

from preprocessing.prepare_dataset import (
    prepare_dataset
)

from preprocessing.splitter import (
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
        n_estimators=300,
        learning_rate=0.05,
        num_leaves=31,
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
        "artifacts/models/lgbm_baseline.pkl"
    )

    print("Model saved.")

    return (
        model,
        X_valid,
        y_valid
    )