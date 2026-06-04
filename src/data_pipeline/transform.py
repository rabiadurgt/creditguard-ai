import numpy as np
import pandas as pd


def basic_cleaning(df: pd.DataFrame):

    df = df.copy()

    df["DAYS_EMPLOYED"] = df["DAYS_EMPLOYED"].replace(
        365243,
        np.nan
    )

    return df