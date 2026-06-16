import numpy as np

from catboost import CatBoostClassifier

from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

from src.preprocessing.prepare_dataset import (
    prepare_dataset
)


def run_cv():

    print("Preparing dataset...")

    df = prepare_dataset(
        "data/processed/train_feature_store.parquet"
    )

    print(df.shape)

    X = df.drop(
        columns=["TARGET"]
    )

    y = df["TARGET"]

    skf = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    scores = []

    for fold, (train_idx, valid_idx) in enumerate(
        skf.split(X, y),
        start=1
    ):

        print(f"\nTraining Fold {fold}...")

        X_train = X.iloc[train_idx]
        X_valid = X.iloc[valid_idx]

        y_train = y.iloc[train_idx]
        y_valid = y.iloc[valid_idx]

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
            verbose=False
        )

        model.fit(
            X_train,
            y_train
        )

        preds = model.predict_proba(
            X_valid
        )[:, 1]

        score = roc_auc_score(
            y_valid,
            preds
        )

        print(
            f"Fold {fold} ROC-AUC: {score:.4f}"
        )

        scores.append(score)

    print("\n" + "=" * 50)

    print(
        f"Mean ROC-AUC: {np.mean(scores):.4f}"
    )

    print(
        f"Std ROC-AUC: {np.std(scores):.4f}"
    )


if __name__ == "__main__":
    run_cv()