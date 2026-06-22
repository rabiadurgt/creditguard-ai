import pandas as pd

DROP_FEATURES = [
    "bb_ever_late",
    "bb_ever_severe_late",
    "bb_recent_max_status",
    "bb_total_severe_late_count",
    "bb_recent_severe_ratio",
    "bb_max_status",
    "bb_total_late_count"
]

def prune_features(df: pd.DataFrame) -> pd.DataFrame:
    cols_to_drop = [c for c in DROP_FEATURES if c in df.columns]
    return df.drop(columns=cols_to_drop)