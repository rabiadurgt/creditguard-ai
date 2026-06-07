import pandas as pd

from src.preprocessing.encoder import (
    encode_categorical_features
)

from src.preprocessing.missing_handler import (
    handle_missing_values
)

def prepare_dataset(
    feature_store_path: str
):

    df = pd.read_parquet(
        feature_store_path
    )

    df = df.drop(
        columns=["SK_ID_CURR"]
    )
    df = handle_missing_values(
        df
    )

    df = encode_categorical_features(
        df
    )

    return df