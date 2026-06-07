import pandas as pd


def get_feature_importance(
    model,
    feature_names
):

    importance_df = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": model.feature_importances_
        }
    )

    importance_df = importance_df.sort_values(
        by="importance",
        ascending=False
    )

    return importance_df