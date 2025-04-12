# app/ml/model.py
import xgboost as xgb
import numpy as np
from abc import ABC, abstractmethod
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import os
import shap
from .gemini import generate, build_diabetes_prompt, build_cardio_prompt
from sklearn.pipeline import Pipeline

class DiseasePredictor(ABC):
    @abstractmethod
    def preprocess(self, data: dict) -> any:
        pass

    @abstractmethod
    def predict(self, preprocessed_data: any) -> dict:
        pass

    @abstractmethod
    def postprocess(self, raw_prediction: dict) -> dict:
        pass

class DiabetesPredictor(DiseasePredictor):
    def __init__(self, model_path: str, scaler_path: str = None):
        if not os.path.exists(model_path):
            raise ValueError(f"Model path {model_path} does not exist.")
            
        self.model = xgb.XGBClassifier()
        self.features = ['AGE', 'Urea', 'Cr', 'HbA1c', 'Chol', 'TG', 'HDL', 'LDL', 'VLDL', 'BMI']
        self.scaler = StandardScaler()
        
        if model_path:
            self.load(model_path, scaler_path)
        
    def preprocess(self, data: dict) -> tuple[np.ndarray, pd.DataFrame]:
        # Convert to dataframe
        df = pd.DataFrame([data])
        df = df[self.features]
        return df.values.flatten(), df

    def predict(self, data: dict, audience: str = "doctor") -> dict:
        _, df = self.preprocess(data)
        
        # Apply scaling
        features_scaled = self.scaler.transform(df)
        
        # Get model predictions
        preds = self.model.predict_proba(features_scaled).reshape(1, -1)[0]
        
        # Get SHAP values
        shap_values = self.explainer.shap_values(df)
        
        # Get original feature values
        original_features = df.iloc[0].to_dict()
        
        # Get basic response
        response = self.postprocess(preds)
        
        # Add SHAP explanation
        explanations = self._format_shap(shap_values, original_features, _class=response["prediction"])
        response["shapley"] = explanations
        
        # Generate prompt and explanation
        prompt = build_diabetes_prompt(
            features_with_shap=explanations,
            prediction=response["prediction"],
            confidence=response["confidence"],
            audience=audience
        )
        
        # Add generated prompt and explanation to response
        response["explanation"] = generate(prompt, audience)
        
        return response

    def postprocess(self, preds: np.ndarray) -> dict:
        confidence = float(preds.max())
        prediction = int(preds.argmax())
        return {"prediction": prediction, "confidence": confidence}
    
    def _format_shap(self, shap_values: list[np.ndarray], features: dict, _class: int) -> list[dict]:
        # Binary classification → use class 1 explanation
        shap_vals = shap_values[0, :, _class] if isinstance(shap_values, np.ndarray) else shap_values[_class]
        
        explanation = []
        for i, (name, value) in enumerate(features.items()):
            explanation.append({
                "feature": name,
                "value": value,
                "shap_value": float(shap_vals[i])
            })
        explanation.sort(key=lambda x: abs(x["shap_value"]), reverse=True)
        # Contribution percentage
        total = sum(abs(x["shap_value"]) for x in explanation)
        for x in explanation:
            x["contribution"] = round(abs(x["shap_value"]) / total * 100, 2)
            
        return explanation
    
    def load(self, model_path: str, scaler_path: str = None):
        """Load model and scaler"""
        # Load the model
        self.model.load_model(model_path)
        self.model.get_booster().feature_names = self.features
        # Load the scaler if path is provided and file exists
        if scaler_path and os.path.exists(scaler_path):
            self.scaler = joblib.load(scaler_path)
        # Create explainer
        self.explainer = shap.TreeExplainer(self.model)

class CardioPredictor(DiseasePredictor):
    def __init__(self, model_path: str):
        if not os.path.exists(model_path):
            raise ValueError(f"Model path {model_path} does not exist.")
        
        self.pipeline: Pipeline = joblib.load(model_path)
        self.model: xgb.XGBClassifier = self.pipeline.named_steps["model"]
        self.preprocessor = self.pipeline.named_steps["preprocessor"]
        self.explainer = shap.TreeExplainer(self.model)

        self.FEATURES: list[str] = [
            'age', 'gender', 'blood_pressure', 'cholesterol_level',
            'exercise_habits', 'smoking', 'family_heart_disease', 'diabetes', 'bmi',
            'high_blood_pressure', 'low_hdl_cholesterol', 'high_ldl_cholesterol',
            'alcohol_consumption', 'stress_level', 'sleep_hours',
            'sugar_consumption', 'triglyceride_level', 'fasting_blood_sugar',
            'crp_level', 'homocysteine_level'
        ]

    def preprocess(self, data: dict) -> tuple[np.ndarray, pd.DataFrame]:
        df: pd.DataFrame = pd.DataFrame([data])
        df = df[self.FEATURES]
        return df.values.flatten(), df

    def predict(self, data: dict, audience: str = "doctor") -> dict:
        _, df = self.preprocess(data)
        
        # Transform input for model prediction
        X_transformed = self.preprocessor.transform(df)
        preds = self.model.predict_proba(X_transformed).reshape(1, -1)[0]
        
        # SHAP values for transformed input
        shap_values = self.explainer.shap_values(X_transformed)
        
        # Get original feature values
        original_features = df.iloc[0].to_dict()

        # Get basic response
        response = self.postprocess(preds)
        
        # Add SHAP explanation
        explanations = self._format_shap(shap_values, original_features, _class=response["prediction"])
        response["shapley"] = explanations
        
        # Generate prompt and explanation
        prompt = build_cardio_prompt(
            features_with_shap=explanations,
            prediction=response["prediction"],
            confidence=response["confidence"],
            audience=audience
        )
        
        # Add generated prompt and explanation to response
        response["explanation"] = generate(prompt, audience)

        return response

    def postprocess(self, preds: np.ndarray) -> dict:
        confidence = float(preds.max())
        prediction = int(preds.argmax())
        return {"prediction": prediction, "confidence": confidence}

    def _format_shap(self, shap_values: list[np.ndarray], features: dict, _class: int) -> list[dict]:
        # Binary classification → use class 1 explanation
        shap_vals = shap_values[_class] if isinstance(shap_values, list) else shap_values[0]

        explanation = []
        for i, (name, value) in enumerate(features.items()):
            explanation.append({
                "feature": name,
                "value": value,
                "shap_value": float(shap_vals[i])  # [0] since single sample
            })
        explanation.sort(key=lambda x: abs(x["shap_value"]), reverse=True)
        # Contribution percentage
        total = sum(abs(x["shap_value"]) for x in explanation)
        for x in explanation:
            x["contribution"] = round(abs(x["shap_value"]) / total * 100, 2)

        return explanation