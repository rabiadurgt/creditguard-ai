import numpy as np
import pandas as pd


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    

    df = df.copy()


    def safe_div(a, b):
        return a / b.replace(0, np.nan)

    # -------------------------------------------------
    # CORE FINANCIAL RATIOS
    # -------------------------------------------------
    df["credit_income_ratio"] = safe_div(df["AMT_CREDIT"], df["AMT_INCOME_TOTAL"])

    df["annuity_income_ratio"] = safe_div(df["AMT_ANNUITY"], df["AMT_INCOME_TOTAL"])

    df["credit_term"] = safe_div(df["AMT_CREDIT"], df["AMT_ANNUITY"])

    df["annuity_credit_ratio"] = safe_div(df["AMT_ANNUITY"], df["AMT_CREDIT"])

    df["income_credit_difference"] = df["AMT_INCOME_TOTAL"] - df["AMT_CREDIT"]

    # -------------------------------------------------
    # AGE / EMPLOYMENT FEATURES
    # -------------------------------------------------
    df["age_years"] = np.abs(df["DAYS_BIRTH"]) / 365

    df["employment_years"] = np.abs(df["DAYS_EMPLOYED"]) / 365

    df["employment_age_ratio"] = safe_div(df["employment_years"], df["age_years"])

    df["is_employed"] = (df["DAYS_EMPLOYED"] > 0).astype(int)

    # -------------------------------------------------
    # FAMILY FEATURES 
    # -------------------------------------------------
    if "CNT_FAM_MEMBERS" in df.columns:
        df["CNT_FAM_MEMBERS"] = df["CNT_FAM_MEMBERS"].replace(0, np.nan)
    else:
        df["CNT_FAM_MEMBERS"] = np.nan

    df["income_per_family_member"] = safe_div(
        df["AMT_INCOME_TOTAL"],
        df["CNT_FAM_MEMBERS"]
    )

    df["child_ratio"] = safe_div(
        df["CNT_CHILDREN"],
        df["CNT_FAM_MEMBERS"]
    )

    df["credit_per_child"] = df["AMT_CREDIT"] / (df["CNT_CHILDREN"] + 1)

    # -------------------------------------------------
    # OWNERSHIP FEATURES
    # -------------------------------------------------
    df["is_car_owner"] = (df["FLAG_OWN_CAR"] == "Y").astype(int)

    df["is_realty_owner"] = (df["FLAG_OWN_REALTY"] == "Y").astype(int)

    # -------------------------------------------------
    # FINAL CLEANUP
    # -------------------------------------------------
    df = df.replace([np.inf, -np.inf], np.nan)

    return df