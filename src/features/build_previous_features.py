import numpy as np
import pandas as pd


def create_previous_features(
    previous: pd.DataFrame
) -> pd.DataFrame:

    # ----------------------------
    # PREPARATION
    # ----------------------------
    previous = previous.copy()

    previous["DAYS_DECISION"] = previous["DAYS_DECISION"].astype(float)
    previous["is_refused"] = (previous["NAME_CONTRACT_STATUS"] == "Refused").astype(int)

    
    previous = previous.sort_values(
        ["SK_ID_CURR", "DAYS_DECISION"]
    )

    # ----------------------------
    # BASE AGG FEATURES
    # ----------------------------
    previous_features = previous.groupby("SK_ID_CURR").agg(

        prev_application_count=(
            "SK_ID_PREV",
            "count"
        ),

        prev_approved_count=(
            "NAME_CONTRACT_STATUS",
            lambda x: (x == "Approved").sum()
        ),

        prev_refused_count=(
            "NAME_CONTRACT_STATUS",
            lambda x: (x == "Refused").sum()
        ),

        prev_canceled_count=(
            "NAME_CONTRACT_STATUS",
            lambda x: (x == "Canceled").sum()
        ),

        prev_avg_application_amount=(
            "AMT_APPLICATION",
            "mean"
        ),

        prev_avg_credit_amount=(
            "AMT_CREDIT",
            "mean"
        ),

        prev_last_application_days=(
            "DAYS_DECISION",
            "max"
        )

    ).reset_index()

    # ----------------------------
    # RATE FEATURES
    # ----------------------------
    previous_features["approval_rate"] = (
        previous_features["prev_approved_count"]
        /
        previous_features["prev_application_count"].replace(0, np.nan)
    )

    previous_features["refusal_rate"] = (
        previous_features["prev_refused_count"]
        /
        previous_features["prev_application_count"].replace(0, np.nan)
    )

    # ----------------------------
    # TREND FEATURES
    # ----------------------------
    credit_trend = previous.groupby("SK_ID_CURR")["AMT_CREDIT"].apply(
        lambda x: x.iloc[-1] - x.iloc[0] if len(x) > 1 else 0
    )

    previous_features["prev_credit_growth"] = previous_features["SK_ID_CURR"].map(
        credit_trend
    )

    # ----------------------------
    # FREQUENCY FEATURES
    # ----------------------------
    avg_days_between = previous.groupby("SK_ID_CURR")["DAYS_DECISION"].apply(
        lambda x: np.mean(np.diff(x)) if len(x) > 1 else np.nan
    )

    previous_features["prev_avg_days_between_apps"] = previous_features["SK_ID_CURR"].map(
        avg_days_between
    )

    # ----------------------------
    # REJECTION STREAK
    # ----------------------------
    def max_rejection_streak(x):
        streak = 0
        max_streak = 0

        for val in x:
            if val == 1:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0

        return max_streak

    rejection_streak = previous.groupby("SK_ID_CURR")["is_refused"].apply(
        max_rejection_streak
    )

    previous_features["prev_max_rejection_streak"] = previous_features["SK_ID_CURR"].map(
        rejection_streak
    )

    # ----------------------------
    # FINAL CLEANUP
    # ----------------------------
    previous_features = previous_features.replace([np.inf, -np.inf], np.nan)

    return previous_features