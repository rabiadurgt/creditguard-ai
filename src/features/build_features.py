import numpy as np
import pandas as pd


def create_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()


    df["credit_income_ratio"] = (
        df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"] # Çekilen kredi / yıllık gelir
    )

    df["annuity_income_ratio"] = (
        df["AMT_ANNUITY"] / df["AMT_INCOME_TOTAL"] # Taksit tutarı / yıllık gelir
    )

    df["credit_term"] = (
        df["AMT_CREDIT"] / df["AMT_ANNUITY"] # Kredi tutarı / taksit tutarı
    )

    df["age_years"] = (
        abs(df["DAYS_BIRTH"]) / 365
    )

    df["employment_years"] = (
        abs(df["DAYS_EMPLOYED"]) / 365
    )

    df["employment_age_ratio"] = (
        df["employment_years"] / df["age_years"]
    )

    df["income_per_family_member"] = (
        df["AMT_INCOME_TOTAL"]
        / df["CNT_FAM_MEMBERS"].replace(0, pd.NA)
    )

    df["child_ratio"] = (
        df["CNT_CHILDREN"]
        / df["CNT_FAM_MEMBERS"].replace(0, pd.NA)
    )

    df["credit_per_child"] = (
        df["AMT_CREDIT"]
        / (df["CNT_CHILDREN"] + 1)
    )

    df["income_credit_difference"] = (
        df["AMT_INCOME_TOTAL"]
        - df["AMT_CREDIT"]
    )

    df["annuity_credit_ratio"] = (
        df["AMT_ANNUITY"]
        / df["AMT_CREDIT"]
    )

    df["is_car_owner"] = (
        df["FLAG_OWN_CAR"] == "Y"
    ).astype(int)

    df["is_realty_owner"] = (
        df["FLAG_OWN_REALTY"] == "Y"
    ).astype(int)

    df["is_employed"] = (
        df["DAYS_EMPLOYED"].notnull()
    ).astype(int)

    return df