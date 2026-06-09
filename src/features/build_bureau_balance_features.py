import pandas as pd


def build_bureau_balance_features(
    bureau_balance: pd.DataFrame,
    bureau: pd.DataFrame
) -> pd.DataFrame:

    df = bureau_balance.copy()

    df["STATUS_NUM"] = (
        df["STATUS"]
        .replace(
            {
                "X": 0,
                "C": 0,
                "0": 0,
                "1": 1,
                "2": 2,
                "3": 3,
                "4": 4,
                "5": 5
            }
        )
        .astype(int)
    )

    df["is_late"] = (
        df["STATUS_NUM"] > 0
    ).astype(int)

    df["is_severe_late"] = (
        df["STATUS_NUM"] >= 3
    ).astype(int)

    bureau_balance_features = (
        df.groupby("SK_ID_BUREAU")
        .agg(
            bb_record_count=(
                "STATUS",
                "count"
            ),
            bb_history_length=(
                "MONTHS_BALANCE",
                lambda x: abs(x.min())
            ),
            bb_late_ratio=(
                "is_late",
                "mean"
            ),
            bb_severe_late_ratio=(
                "is_severe_late",
                "mean"
            ),
            bb_max_status=(
                "STATUS_NUM",
                "max"
            )
        )
        .reset_index()
    )

    bureau_with_balance = (
        bureau[
            [
                "SK_ID_BUREAU",
                "SK_ID_CURR"
            ]
        ]
        .merge(
            bureau_balance_features,
            on="SK_ID_BUREAU",
            how="left"
        )
    )

    customer_features = (
        bureau_with_balance
        .groupby("SK_ID_CURR")
        .agg(
            bb_record_count=(
                "bb_record_count",
                "sum"
            ),
            bb_history_length=(
                "bb_history_length",
                "mean"
            ),
            bb_late_ratio=(
                "bb_late_ratio",
                "mean"
            ),
            bb_severe_late_ratio=(
                "bb_severe_late_ratio",
                "mean"
            ),
            bb_max_status=(
                "bb_max_status",
                "max"
            )
        )
        .reset_index()
    )

    return customer_features