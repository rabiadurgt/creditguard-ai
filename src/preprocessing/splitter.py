from sklearn.model_selection import train_test_split


def split_dataset(
    df,
    target_column="TARGET",
    test_size=0.2,
    random_state=42
):

    X = df.drop(
        columns=[target_column]
    )

    y = df[target_column]

    X_train, X_valid, y_train, y_valid = train_test_split(
        X,
        y,
        test_size=test_size,
        stratify=y,
        random_state=random_state
    )

    return (
        X_train,
        X_valid,
        y_train,
        y_valid
    )