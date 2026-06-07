import numpy as np
import pandas as pd


def build_installment_features(
    installments: pd.DataFrame
):

    df = installments.copy()

    df["days_late"] = (
        df["DAYS_ENTRY_PAYMENT"]
        - df["DAYS_INSTALMENT"]
    )

    df["days_late"] = (
        df["days_late"]
        .clip(lower=0)
    )

    df["is_late"] = (
        df["days_late"] > 0
    ).astype(int)

    df["payment_ratio"] = (
        df["AMT_PAYMENT"] / df["AMT_INSTALMENT"].replace(0,np.nan)
    )

    installment_features = (
        df.groupby("SK_ID_CURR")
        .agg(
            installment_count=(
                "NUM_INSTALMENT_NUMBER",
                "count"
            ),
            avg_days_late=(
                "days_late",
                "mean"
            ),
            max_days_late=(
                "days_late",
                "max"
            ),
            late_payment_count=(
                "is_late",
                "sum"
            ),
            late_payment_ratio=(
                "is_late",
                "mean"
            ),
            avg_payment_ratio=(
                "payment_ratio",
                "mean"
            ),
            total_payment_amount=(
                "AMT_PAYMENT",
                "sum"
            )
        )
        .reset_index()
    )

    return installment_features