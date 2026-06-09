import pandas as pd


def merge_features(
    application_df: pd.DataFrame,
    bureau_features: pd.DataFrame,
    previous_features: pd.DataFrame,
    installment_features: pd.DataFrame,
    pos_features: pd.DataFrame,
    credit_card_features: pd.DataFrame,
    bureau_balance_features: pd.DataFrame
) -> pd.DataFrame:

    df = application_df.copy()

    df = df.merge(
        bureau_features,
        on="SK_ID_CURR",
        how="left"
    )

    df = df.merge(
        previous_features,
        on="SK_ID_CURR",
        how="left"
    )

    df = df.merge(
        installment_features,
        on="SK_ID_CURR",
        how="left"
    )

    df = df.merge(
        pos_features,
        on="SK_ID_CURR",
        how="left"
    )

    df = df.merge(
        credit_card_features,
        on="SK_ID_CURR",
        how="left"
    )

    df = df.merge(
        bureau_balance_features,
        on="SK_ID_CURR",
        how="left"
    )
    
    return df