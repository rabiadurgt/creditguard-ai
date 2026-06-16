'''
LightGBM tahmini
+
CatBoost tahmini
=
Tek bir ensemble tahmini
'''

import joblib

from sklearn.metrics import roc_auc_score

from src.preprocessing.prepare_dataset import (
    prepare_dataset
)

from src.preprocessing.splitter import (
    split_dataset
)


def evaluate_blend():

    print("Preparing dataset...")

    df = prepare_dataset(
        "data/processed/train_feature_store.parquet"
    )

    X_train, X_valid, y_train, y_valid = (
        split_dataset(df)
    )

    print(
        f"Validation shape: {X_valid.shape}"
    )

    print(
        "Loading models..."
    )

    lgb_model = joblib.load(
        "artifacts/models/lgbm_optuna_cv.pkl"
    )

    cat_model = joblib.load(
        "artifacts/models/catboost_baseline.pkl"
    )

    print(
        "Generating predictions..."
    )

    lgb_preds = (
        lgb_model
        .predict_proba(X_valid)[:, 1]
    )

    cat_preds = (
        cat_model
        .predict_proba(X_valid)[:, 1]
    )

    blend_preds = (
        0.5 * lgb_preds +
        0.5 * cat_preds
    )

    lgb_auc = roc_auc_score(
        y_valid,
        lgb_preds
    )

    cat_auc = roc_auc_score(
        y_valid,
        cat_preds
    )

    blend_auc = roc_auc_score(
        y_valid,
        blend_preds
    )

    print()

    print(
        f"LightGBM ROC-AUC: {lgb_auc:.4f}"
    )

    print(
        f"CatBoost ROC-AUC: {cat_auc:.4f}"
    )

    print(
        f"Blend ROC-AUC: {blend_auc:.4f}"
    )


if __name__ == "__main__":
    evaluate_blend()