import pandas as pd

from src.preprocessing.encoder import encode_categorical_features
from src.preprocessing.missing_handler import handle_missing_values
from src.feature_store.final_features import FINAL_FEATURES


def prepare_dataset(feature_store_path: str):

    df = pd.read_parquet(feature_store_path)

    # ID drop
    if "SK_ID_CURR" in df.columns:
        df = df.drop(columns=["SK_ID_CURR"])

    # missing + encoding
    df = handle_missing_values(df)
    df = encode_categorical_features(df)

    # FEATURE FREEZE
    available_features = [
        c for c in FINAL_FEATURES
        if c in df.columns
    ]

    df = df[available_features + ["TARGET"]]

    return df
