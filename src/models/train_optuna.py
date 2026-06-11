import optuna
import lightgbm as lgb
import numpy as np

from sklearn.metrics import (
    roc_auc_score
)

from sklearn.model_selection import (
    StratifiedKFold
)

from src.preprocessing.prepare_dataset import (
    prepare_dataset
)


print("Preparing dataset...")

df = prepare_dataset(
    "data/processed/train_feature_store.parquet"
)

X = df.drop(
    columns=["TARGET"]
)

y = df["TARGET"]

print(X.shape)


def objective(trial):

    params = {

        "n_estimators": trial.suggest_int(
            "n_estimators",
            300,
            1500
        ),

        "learning_rate": trial.suggest_float(
            "learning_rate",
            0.01,
            0.1
        ),

        "num_leaves": trial.suggest_int(
            "num_leaves",
            20,
            200
        ),

        "max_depth": trial.suggest_int(
            "max_depth",
            3,
            12
        ),

        "min_child_samples": trial.suggest_int(
            "min_child_samples",
            20,
            200
        ),

        "subsample": trial.suggest_float(
            "subsample",
            0.6,
            1.0
        ),

        "colsample_bytree": trial.suggest_float(
            "colsample_bytree",
            0.6,
            1.0
        ),

        "reg_alpha": trial.suggest_float(
            "reg_alpha",
            0.0,
            5.0
        ),

        "reg_lambda": trial.suggest_float(
            "reg_lambda",
            0.0,
            5.0
        ),

        "objective": "binary",
        "metric": "auc",
        "verbosity": -1,
        "random_state": 42,
        "n_jobs": -1
    }

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    scores = []

    for train_idx, valid_idx in cv.split(X, y):

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

        model = lgb.LGBMClassifier(
            **params
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

        scores.append(
            auc
        )

    mean_auc = np.mean(
        scores
    )

    return mean_auc


if __name__ == "__main__":

    study = optuna.create_study(
        direction="maximize"
    )

    study.optimize(
        objective,
        n_trials=10   #20
    )

    print("\nBest ROC-AUC:")
    print(study.best_value)

    print("\nBest Params:")
    print(study.best_params)