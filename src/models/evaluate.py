from sklearn.metrics import (
    roc_auc_score
)


def evaluate_model(
    model,
    X_valid,
    y_valid
):

    probabilities = model.predict_proba(
        X_valid
    )[:, 1]

    auc = roc_auc_score(
        y_valid,
        probabilities
    )

    print(
        f"Validation ROC-AUC: {auc:.4f}"
    )

    return auc