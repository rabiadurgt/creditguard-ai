import pandas as pd
import numpy as np


def create_bureau_features(bureau: pd.DataFrame) -> pd.DataFrame:

    bureau_features = bureau.groupby("SK_ID_CURR").agg(

        bureau_total_credit=("AMT_CREDIT_SUM", "sum"),
        bureau_total_debt=("AMT_CREDIT_SUM_DEBT", "sum"),

        bureau_active_loans=("CREDIT_ACTIVE", lambda x: (x == "Active").sum()),
        bureau_closed_loans=("CREDIT_ACTIVE", lambda x: (x == "Closed").sum()),

        bureau_overdue_amount=("AMT_CREDIT_SUM_OVERDUE", "sum"),
    ).reset_index()

    # -------------------------------------------------
    # 
    # -------------------------------------------------
    total_loans = (
        bureau_features["bureau_active_loans"] +
        bureau_features["bureau_closed_loans"]
    ).replace(0, np.nan)

    active_loans = bureau_features["bureau_active_loans"].replace(0, np.nan)

    # -------------------------------------------------
    # RATIOS
    # -------------------------------------------------
    bureau_features["bureau_debt_credit_ratio"] = (
        bureau_features["bureau_total_debt"] /
        bureau_features["bureau_total_credit"].replace(0, np.nan)
    )

    bureau_features["bureau_avg_credit_per_loan"] = (
        bureau_features["bureau_total_credit"] / total_loans
    )

    bureau_features["bureau_avg_debt_per_loan"] = (
        bureau_features["bureau_total_debt"] / total_loans
    )

    bureau_features["bureau_active_loan_ratio"] = (
        bureau_features["bureau_active_loans"] / total_loans
    )

    bureau_features["bureau_credit_per_active_loan"] = (
        bureau_features["bureau_total_credit"] / active_loans
    )

    bureau_features["bureau_debt_per_active_loan"] = (
        bureau_features["bureau_total_debt"] / active_loans
    )

   
    bureau_features = bureau_features.replace([np.inf, -np.inf], np.nan)

    return bureau_features