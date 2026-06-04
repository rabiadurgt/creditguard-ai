import pandas as pd
from sklearn.preprocessing import LabelEncoder


def encode_categorical_features(
    df: pd.DataFrame
) -> pd.DataFrame:

    df = df.copy()

    categorical_cols = df.select_dtypes(
        include="object"
    ).columns

    for col in categorical_cols:

        encoder = LabelEncoder()

        df[col] = encoder.fit_transform(
            df[col].astype(str)
        )

    return df