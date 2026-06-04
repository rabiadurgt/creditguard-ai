import numpy as np
import pandas as pd


def handle_missing_values(
    df: pd.DataFrame
) -> pd.DataFrame:

    df = df.copy()

    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    numeric_cols = df.select_dtypes(
        include=["number"]
    ).columns

    for col in numeric_cols:

        df[col] = df[col].fillna(
            df[col].median()
        )

    return df