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

    df["is_severe_late"] = (
        df["days_late"] >= 30
    ).astype(int)

    df["payment_ratio"] = (
        df["AMT_PAYMENT"] / df["AMT_INSTALMENT"].replace(0,np.nan)
    )
    recent_12m = df[
        df["DAYS_INSTALMENT"] >= -365
    ].copy()

    recent_6m = df[
        df["DAYS_INSTALMENT"] >= -180
    ].copy()

    recent_12m_features = (
        recent_12m
        .groupby("SK_ID_CURR")
        .agg(
            recent_12m_late_ratio=(
                "is_late",
                "mean"
            )
        )
    )

    recent_6m_features = (
        recent_6m
        .groupby("SK_ID_CURR")
        .agg(
            recent_6m_late_ratio=(
                "is_late",
                "mean"
            )
        )
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
            median_days_late=(
                "days_late",
                "median"
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
            severe_late_count=(
                "is_severe_late",
                "sum"
            ),
            severe_late_ratio=(
                "is_severe_late",
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
    )

    installment_features = (
        installment_features
        .join(recent_12m_features)
        .join(recent_6m_features)
        .reset_index()
    )
    return installment_features