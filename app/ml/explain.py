# app/explain/shap_exp.py
import shap
import numpy as np

class ShapExplainer:
    def __init__(self, model):
        self.explainer = shap.TreeExplainer(model)
    
    def explain(self, data: np.ndarray):
        shap_values = self.explainer.shap_values(data)
        return shap_values

# Example instantiation can occur during startup:
# from app.ml.model import model_instance
# shap_explainer = ShapExplainer(model_instance.model)
