import optuna
import lightgbm as lgb

from sklearn.metrics import roc_auc_score

from src.preprocessing.prepare_dataset import (
    prepare_dataset
)

from src.preprocessing.splitter import (
    split_dataset
)

print("Preparing dataset...")

df = prepare_dataset(
    "data/processed/train_feature_store.parquet"
)

X_train, X_valid, y_train, y_valid = (
    split_dataset(df)
)

print(
    f"Train shape: {X_train.shape}"
)

print(
    f"Validation shape: {X_valid.shape}"
)


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

        "random_state": 42,
        "n_jobs": -1
    }

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

    score = roc_auc_score(
        y_valid,
        preds
    )

    return score


if __name__ == "__main__":

    study = optuna.create_study(
        direction="maximize"
    )

    study.optimize(
        objective,
        n_trials=10
    )

    print(
        "Best ROC-AUC:",
        study.best_value
    )

    print(
        "Best Params:"
    )

    print(
        study.best_params
    )