import numpy as np
import pandas as pd


def create_previous_features(
    previous: pd.DataFrame
) -> pd.DataFrame:

    previous_features = previous.groupby(
        "SK_ID_CURR"
    ).agg(

        # Müşteri kaç kez başvuru yaptı?
        prev_application_count=(
            "SK_ID_PREV",
            "count"
        ),

        # Kaç başvuru onaylandı?
        prev_approved_count=(
            "NAME_CONTRACT_STATUS",
            lambda x: (x == "Approved").sum()
        ),

        # Kaç başvuru reddedildi?
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
        )

    ).reset_index()

    # Onaylanan Başvuru / Toplam Başvuru
    previous_features["approval_rate"] = (
        previous_features["prev_approved_count"]
        /
        previous_features["prev_application_count"]
    )

    # Reddedilen Başvuru / Toplam Başvuru
    previous_features["refusal_rate"] = (
        previous_features["prev_refused_count"]
        /
        previous_features["prev_application_count"]
    )

    return previous_features