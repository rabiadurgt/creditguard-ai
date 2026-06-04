from models.train import (
    train_model
)

from models.evaluate import (
    evaluate_model
)


def main():

    model, X_valid, y_valid = (
        train_model()
    )

    evaluate_model(
        model,
        X_valid,
        y_valid
    )


if __name__ == "__main__":
    main()