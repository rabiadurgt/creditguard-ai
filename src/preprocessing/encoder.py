import pandas as pd

def encode_categorical_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    categorical_cols = df.select_dtypes(include="object").columns

    for col in categorical_cols:
        df[col] = df[col].astype("category").cat.codes

    return df