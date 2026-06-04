import pandas as pd
import numpy as np

def create_bureau_features(
    bureau: pd.DataFrame
) -> pd.DataFrame:

    bureau_features = bureau.groupby(
        "SK_ID_CURR"
    ).agg(
        # Müşterinin diğer kurumlardaki toplam kredi hacmi
        bureau_total_credit=(
            "AMT_CREDIT_SUM",
            "sum"
        ),
        # Müşterinin mevcut toplam borcu
        bureau_total_debt=(
            "AMT_CREDIT_SUM_DEBT",
            "sum"
        ),

        bureau_active_loans=(
            "CREDIT_ACTIVE",
            lambda x: (x == "Active").sum()
        ),

        bureau_closed_loans=(
            "CREDIT_ACTIVE",
            lambda x: (x == "Closed").sum()
        ),

        bureau_overdue_amount=(
            "AMT_CREDIT_SUM_OVERDUE",
            "sum"
        )
    ).reset_index()

    bureau_features["bureau_debt_credit_ratio"] = (
        bureau_features["bureau_total_debt"]
        /
        bureau_features["bureau_total_credit"].replace(0, np.nan)
    )

    bureau_features["bureau_debt_credit_ratio"] = (
        bureau_features["bureau_debt_credit_ratio"]
        .replace([np.inf, -np.inf],np.nan
        )
    )
    

    return bureau_features