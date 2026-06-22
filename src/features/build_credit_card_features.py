import numpy as np
import pandas as pd


def build_credit_card_features(
    credit_card: pd.DataFrame
) -> pd.DataFrame:

    df = credit_card.copy()

    # --------------------------------------------------
    # 1. BASIC DERIVED FEATURES
    # --------------------------------------------------

    df["credit_utilization_ratio"] = (
        df["AMT_BALANCE"]
        / df["AMT_CREDIT_LIMIT_ACTUAL"].replace(0, np.nan)
    )

    df["high_utilization"] = (df["credit_utilization_ratio"] > 0.8).astype(int)
    df["very_high_utilization"] = (df["credit_utilization_ratio"] > 1.0).astype(int)

    df["has_dpd"] = (df["SK_DPD"] > 0).astype(int)
    df["severe_dpd"] = (df["SK_DPD"] > 30).astype(int)

    # --------------------------------------------------
    # 2. SORT (time aware)
    # --------------------------------------------------

    df = df.sort_values(
        ["SK_ID_CURR", "MONTHS_BALANCE"],
        ascending=[True, True]
    )

    # --------------------------------------------------
    # 3. RECENCY WINDOWS
    # --------------------------------------------------

    recent_6m = df[df["MONTHS_BALANCE"] >= -6]
    recent_12m = df[df["MONTHS_BALANCE"] >= -12]

    # --------------------------------------------------
    # 4. TREND FEATURE (CRITICAL)
    # --------------------------------------------------

    trend = (
        df.groupby("SK_ID_CURR")["AMT_BALANCE"]
        .apply(
            lambda x: np.polyfit(range(len(x)), x, 1)[0]
            if len(x) > 2 else 0
        )
        .rename("cc_balance_trend")
    )

    # --------------------------------------------------
    # 5. MAIN AGGREGATIONS
    # --------------------------------------------------

    credit_card_features = (
        df.groupby("SK_ID_CURR")
        .agg(

            cc_record_count=("SK_ID_PREV", "count"),

            # balance
            cc_avg_balance=("AMT_BALANCE", "mean"),
            cc_max_balance=("AMT_BALANCE", "max"),

            # credit limit
            cc_avg_credit_limit=("AMT_CREDIT_LIMIT_ACTUAL", "mean"),

            # utilization
            cc_utilization_ratio=("credit_utilization_ratio", "mean"),
            cc_max_utilization=("credit_utilization_ratio", "max"),

            # risk behavior
            cc_high_util_ratio=("high_utilization", "mean"),
            cc_very_high_util_ratio=("very_high_utilization", "mean"),

            # dpd behavior
            cc_avg_dpd=("SK_DPD", "mean"),
            cc_max_dpd=("SK_DPD", "max"),
            cc_dpd_ratio=("has_dpd", "mean"),
            cc_severe_dpd_ratio=("severe_dpd", "mean"),

            # payments
            cc_avg_payment=("AMT_PAYMENT_TOTAL_CURRENT", "mean"),
            cc_total_payment=("AMT_PAYMENT_TOTAL_CURRENT", "sum"),

            # drawings
            cc_avg_drawings=("AMT_DRAWINGS_CURRENT", "mean")
        )
        .reset_index()
    )

    # --------------------------------------------------
    # 6. JOIN TREND + RECENCY
    # --------------------------------------------------

    recent_6m_features = recent_6m.groupby("SK_ID_CURR").agg(
        cc_6m_util_ratio=("credit_utilization_ratio", "mean"),
        cc_6m_dpd_ratio=("has_dpd", "mean")
    )

    recent_12m_features = recent_12m.groupby("SK_ID_CURR").agg(
        cc_12m_util_ratio=("credit_utilization_ratio", "mean"),
        cc_12m_dpd_ratio=("has_dpd", "mean")
    )

    credit_card_features = credit_card_features.join(trend, on="SK_ID_CURR")
    credit_card_features = credit_card_features.join(recent_6m_features, on="SK_ID_CURR")
    credit_card_features = credit_card_features.join(recent_12m_features, on="SK_ID_CURR")

    return credit_card_features