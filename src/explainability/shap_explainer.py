import shap
import pandas as pd


class SHAPExplainer:

    def __init__(self, model, background_data: pd.DataFrame):

        self.model = model
        self.background_data = background_data

        self.explainer = None
        self.feature_names = background_data.columns

    def _init_explainer(self):

        if self.explainer is None:
            self.explainer = shap.TreeExplainer(
                self.model,
                data=self.background_data,
                feature_perturbation="interventional"
            )

    def explain(self, X: pd.DataFrame, top_k: int = 5):

        self._init_explainer()

        shap_values = self.explainer.shap_values(X)

        if isinstance(shap_values, list):
            shap_values = shap_values[1]

        values = shap_values[0]
        features = X.iloc[0]

        explanation_pairs = list(zip(self.feature_names, values))

        explanation_pairs = sorted(
            explanation_pairs,
            key=lambda x: abs(x[1]),
            reverse=True
        )

        top_features = explanation_pairs[:top_k]

        return [
            f"{feat}: impact {round(val, 4)}"
            for feat, val in top_features
        ]