import shap
import pandas as pd
import matplotlib.pyplot as plt
from xgboost import XGBRegressor


class ESGExplainability:
    """
    Explainability module for SME ESG prediction.
    Uses SHAP to compute and visualize feature contributions.
    """

    def __init__(self, model: XGBRegressor, X_train: pd.DataFrame):
        self.model = model
        self.X_train = X_train
        self.explainer = shap.Explainer(model, X_train)

    def explain_instance(self, instance: pd.DataFrame):
        """
        Explain a single SME ESG prediction.
        """
        shap_values = self.explainer(instance)
        return shap_values

    def plot_global_importance(self):
        """
        Global ESG indicator importance.
        """
        shap_values = self.explainer(self.X_train)
        plt.figure()
        shap.plots.bar(shap_values, show=False)
        plt.tight_layout()
        return plt

    def plot_beeswarm(self):
        """
        Distribution of ESG indicator effects.
        """
        shap_values = self.explainer(self.X_train)
        plt.figure()
        shap.plots.beeswarm(shap_values, show=False)
        plt.tight_layout()
        return plt