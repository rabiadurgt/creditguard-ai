import numpy as np
import lightgbm as lgb

from sklearn.model_selection import (
    StratifiedKFold
)

from sklearn.metrics import (
    roc_auc_score
)

from src.preprocessing.prepare_dataset import (
    prepare_dataset
)


def run_cross_validation():

    print(
        "Preparing dataset..."
    )

    df = prepare_dataset(
        "data/processed/train_feature_store.parquet"
    )

    print(df.shape)

    X = df.drop(
        columns=["TARGET"]
    )

    y = df["TARGET"]

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    scores = []

    for fold, (
        train_idx,
        valid_idx
    ) in enumerate(
        cv.split(X, y),
        start=1
    ):

        print(f"\nTraining Fold {fold}...")

        X_train = X.iloc[
            train_idx
        ]

        X_valid = X.iloc[
            valid_idx
        ]

        y_train = y.iloc[
            train_idx
        ]

        y_valid = y.iloc[
            valid_idx
        ]

        print(f"Train shape: {X_train.shape}")

        print(f"Validation shape: {X_valid.shape}")

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

        model.fit(
            X_train,
            y_train
        )

        preds = model.predict_proba(
            X_valid
        )[:, 1]

        auc = roc_auc_score(
            y_valid,
            preds
        )

        scores.append(auc)

        print(f"Fold {fold} ROC-AUC: {auc:.4f}")

    print("\n" + "=" * 50)

    print(f"Mean ROC-AUC: {np.mean(scores):.4f}")

    print(f"Std ROC-AUC: {np.std(scores):.4f}")

    print("=" * 50)


if __name__ == "__main__":
    run_cross_validation()