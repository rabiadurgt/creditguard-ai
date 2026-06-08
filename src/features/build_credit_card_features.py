import numpy as np
import pandas as pd


def build_credit_card_features(
    credit_card: pd.DataFrame
) -> pd.DataFrame:

    df = credit_card.copy()

    df["credit_utilization_ratio"] = (
        df["AMT_BALANCE"]
        /
        df["AMT_CREDIT_LIMIT_ACTUAL"].replace(
            0,
            np.nan
        )
    )

    credit_card_features = (
        df.groupby("SK_ID_CURR")
        .agg(
            cc_record_count=(
                "SK_ID_PREV",
                "count"
            ),

            cc_avg_balance=(
                "AMT_BALANCE",
                "mean"
            ),

            cc_max_balance=(
                "AMT_BALANCE",
                "max"
            ),

            cc_avg_credit_limit=(
                "AMT_CREDIT_LIMIT_ACTUAL",
                "mean"
            ),

            cc_utilization_ratio=(
                "credit_utilization_ratio",
                "mean"
            ),

            cc_avg_payment=(
                "AMT_PAYMENT_TOTAL_CURRENT",
                "mean"
            ),

            cc_total_payment=(
                "AMT_PAYMENT_TOTAL_CURRENT",
                "sum"
            ),

            cc_avg_dpd=(
                "SK_DPD",
                "mean"
            ),

            cc_max_dpd=(
                "SK_DPD",
                "max"
            ),

            cc_avg_drawings=(
                "AMT_DRAWINGS_CURRENT",
                "mean"
            )
        )
        .reset_index()
    )

    return credit_card_features