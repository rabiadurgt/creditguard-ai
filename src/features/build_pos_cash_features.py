import pandas as pd


def build_pos_cash_features(
    pos: pd.DataFrame
) -> pd.DataFrame:

    pos_features = pd.DataFrame()

    pos_features["pos_record_count"] = (
        pos.groupby("SK_ID_CURR")
           .size()
    )

    pos_features["pos_avg_dpd"] = (
        pos.groupby("SK_ID_CURR")["SK_DPD"]
           .mean()
    )

    pos_features["pos_max_dpd"] = (
        pos.groupby("SK_ID_CURR")["SK_DPD"]
           .max()
    )

    pos_features["pos_avg_dpd_def"] = (
        pos.groupby("SK_ID_CURR")["SK_DPD_DEF"]
           .mean()
    )

    pos_features["pos_max_dpd_def"] = (
        pos.groupby("SK_ID_CURR")["SK_DPD_DEF"]
           .max()
    )

    pos_features["pos_active_contracts"] = (
        pos[
            pos["NAME_CONTRACT_STATUS"]
            == "Active"
        ]
        .groupby("SK_ID_CURR")
        .size()
    )

    pos_features["pos_completed_contracts"] = (
        pos[
            pos["NAME_CONTRACT_STATUS"]
            == "Completed"
        ]
        .groupby("SK_ID_CURR")
        .size()
    )

    pos_features["pos_avg_future_installments"] = (
        pos.groupby("SK_ID_CURR")
           ["CNT_INSTALMENT_FUTURE"]
           .mean()
    )

    pos_features = (
        pos_features
        .reset_index()
    )

    return pos_features