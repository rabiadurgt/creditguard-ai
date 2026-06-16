from src.models.train_catboost import (
    train_catboost
)

from src.models.evaluate import (
    evaluate_model
)


def main():

    model, X_valid, y_valid = (
        train_catboost()
    )

    evaluate_model(
        model,
        X_valid,
        y_valid
    )


if __name__ == "__main__":
    main()