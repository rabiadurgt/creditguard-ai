import pandas as pd
import numpy as np


def build_bureau_balance_features(
    bureau_balance: pd.DataFrame,
    bureau: pd.DataFrame
) -> pd.DataFrame:

    df = bureau_balance.copy()

    # -----------------------
    # 1. Encoding
    # -----------------------
    df["STATUS_NUM"] = (
        df["STATUS"]
        .replace({
            "X": 0,
            "C": 0,
            "0": 0,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5
        })
        .astype(int)
    )

    df["is_late"] = (df["STATUS_NUM"] > 0).astype(int)
    df["is_severe_late"] = (df["STATUS_NUM"] >= 3).astype(int)

    # -----------------------
    # 2. Sort (time aware)
    # -----------------------
    df = df.sort_values(
        ["SK_ID_BUREAU", "MONTHS_BALANCE"],
        ascending=[True, True]   # IMPORTANT: time forward
    )

    # -----------------------
    # 3. Rolling windows
    # -----------------------
    recent_12m = df[df["MONTHS_BALANCE"] >= -12]
    recent_6m = df[df["MONTHS_BALANCE"] >= -6]
    recent_3m = df[df["MONTHS_BALANCE"] >= -3]

    # -----------------------
    # 4. BASE FEATURES (level)
    # -----------------------
    base_features = df.groupby("SK_ID_BUREAU").agg(
        bb_record_count=("STATUS", "count"),
        bb_late_ratio=("is_late", "mean"),
        bb_severe_late_ratio=("is_severe_late", "mean"),
        bb_max_status=("STATUS_NUM", "max"),
        bb_total_late_count=("is_late", "sum"),
        bb_total_severe_late_count=("is_severe_late", "sum"),
        bb_ever_late=("is_late", "max"),
        bb_ever_severe_late=("is_severe_late", "max"),
        bb_history_length=("MONTHS_BALANCE",lambda x: abs(x.min())),
    )

    # -----------------------
    # 5. RECENCY FEATURES
    # -----------------------
    recent_features = recent_12m.groupby("SK_ID_BUREAU").agg(
        bb_recent_late_ratio=("is_late", "mean"),
        bb_recent_severe_ratio=("is_severe_late", "mean"),
        bb_recent_late_count=("is_late", "sum"),
        bb_recent_max_status=("STATUS_NUM", "max"),
    )

    recent_6m_features = recent_6m.groupby("SK_ID_BUREAU").agg(
        bb_6m_late_ratio=("is_late", "mean")
    )

    recent_3m_features = recent_3m.groupby("SK_ID_BUREAU").agg(
        bb_3m_late_ratio=("is_late", "mean")
    )

    # -----------------------
    # 6. TREND FEATURES (NEW - CRITICAL)
    # -----------------------
    trend_features = df.groupby("SK_ID_BUREAU")["STATUS_NUM"].agg(
        bb_status_mean="mean",
        bb_status_std="std"
    )

    # slope approximation (simple trend)
    trend_slope = (
        df.groupby("SK_ID_BUREAU")
        .apply(lambda x: np.polyfit(x["MONTHS_BALANCE"], x["STATUS_NUM"], 1)[0]
               if len(x) > 2 else 0)
        .rename("bb_status_trend")
    )

    # -----------------------
    # 7. RECENCY SIGNAL (last observation)
    # -----------------------
    last_status = (
        df.groupby("SK_ID_BUREAU")["STATUS_NUM"]
        .last()
        .rename("bb_last_status")
    )

    # months since last late
    last_late = (
        df[df["is_late"] == 1]
        .groupby("SK_ID_BUREAU")["MONTHS_BALANCE"]
        .max()
        .abs()
        .rename("bb_months_since_last_late")
    )

    # -----------------------
    # 8. MERGE ALL BUREAU LEVEL
    # -----------------------
    
    bureau_balance_features = base_features

    for f in [
        recent_features,
        recent_6m_features,
        recent_3m_features,
        trend_features,
        trend_slope,
        last_status,
        last_late
    ]:
        bureau_balance_features = bureau_balance_features.join(f, how="left")

    bureau_balance_features = bureau_balance_features.reset_index()
    
    # -----------------------
    # 9. MAP TO CUSTOMER LEVEL
    # -----------------------
    bureau_with_balance = bureau[
        ["SK_ID_BUREAU", "SK_ID_CURR"]
    ].merge(
        bureau_balance_features,
        on="SK_ID_BUREAU",
        how="left"
    )

    customer_features = bureau_with_balance.groupby("SK_ID_CURR").agg(
        bb_record_count=("bb_record_count", "sum"),

        bb_late_ratio=("bb_late_ratio", "mean"),
        bb_severe_late_ratio=("bb_severe_late_ratio", "mean"),

        bb_recent_late_ratio=("bb_recent_late_ratio", "mean"),
        bb_6m_late_ratio=("bb_6m_late_ratio", "mean"),
        bb_3m_late_ratio=("bb_3m_late_ratio", "mean"),

        bb_status_std=("bb_status_std", "mean"),
        bb_status_trend=("bb_status_trend", "mean"),
        bb_status_mean=("bb_status_mean","mean"),

        bb_last_status=("bb_last_status", "max"),
        bb_months_since_last_late=("bb_months_since_last_late", "mean"),

        bb_ever_late=("bb_ever_late", "max"),
        bb_ever_severe_late=("bb_ever_severe_late", "max"),
        bb_max_status=(
            "bb_max_status",
            "max"
        ),

        bb_recent_max_status=(
            "bb_recent_max_status",
            "max"
        ),

        bb_recent_late_count=(
            "bb_recent_late_count",
            "sum"
        ),

        bb_total_late_count=(
            "bb_total_late_count",
            "sum"
        ),

        bb_total_severe_late_count=(
            "bb_total_severe_late_count",
            "sum"
        ),
        bb_history_length=(
            "bb_history_length",
            "mean"
        ),
        bb_recent_severe_ratio=(
            "bb_recent_severe_ratio",
            "mean"
        ),

    ).reset_index()

    return customer_features