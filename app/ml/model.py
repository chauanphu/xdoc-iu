# app/ml/model.py
import xgboost as xgb
import numpy as np
from abc import ABC, abstractmethod
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import os
import shap
from .gemini import generate, prepare_prompt
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
        self.model = xgb.XGBClassifier()
        self.features = ['AGE', 'Urea', 'Cr', 'HbA1c', 'Chol', 'TG', 'HDL', 'LDL', 'VLDL', 'BMI']
        self.scaler = StandardScaler()
        if model_path:
            self.load(model_path, scaler_path)
        
    def preprocess(self, data: dict) -> np.ndarray:
        # Convert to dataframe
        df = pd.DataFrame([data])
        df = df[self.features]
        features = df.values
        features_scaled = self.scaler.transform(df)
        return features.flatten(), features_scaled, df

    def predict(self, data: np.ndarray) -> dict:
        raw_features, features_scaled, df = self.preprocess(data)
        preds = self.model.predict_proba(features_scaled).reshape(1, -1)[0]
        shap_values = self.explainer.shap_values(df)
        response = self.postprocess(preds, shap_values, raw_features=raw_features)
        return response

    def postprocess(self, raw_prediction, shap_values: np.ndarray, raw_features: np.ndarray) -> dict:
        preds = raw_prediction
        confidence = float(preds.max())
        prediction = int(preds.argmax())
        values = shap_values[0, :, prediction]
        prompt = prepare_prompt(
            columns=self.features, 
            predicted_class=prediction, 
            probabilities=preds, 
            shap_values=values, 
            raw_data=raw_features
        )
        # Convert shap values to a dictionary
        values = values.flatten().tolist()
        feature_sign = {feature: shap_value for feature, shap_value in zip(self.features, values)}
        # Generate explanation using Gemini
        explanation = generate(prompt)
        return {
            "prediction": prediction, 
            "confidence": confidence,
            "shapley": feature_sign,
            "explanation": explanation
        }
    
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
        self.pipelie: Pipeline = joblib.load(model_path)
        self.model: xgb.XGBClassifier = self.pipelie.named_steps["model"]
        self.explainer = shap.TreeExplainer(self.model)
        self.preprocessor = self.pipelie.named_steps["preprocessor"]
        self.FEATURES: list[str] = ['age', 'gender', 'blood_pressure', 'cholesterol_level',
       'exercise_habits', 'smoking', 'family_heart_disease', 'diabetes', 'bmi',
       'high_blood_pressure', 'low_hdl_cholesterol', 'high_ldl_cholesterol',
       'alcohol_consumption', 'stress_level', 'sleep_hours',
       'sugar_consumption', 'triglyceride_level', 'fasting_blood_sugar',
       'crp_level', 'homocysteine_level']

    def preprocess(self, data: dict) -> np.ndarray:
        df: pd.DataFrame = pd.DataFrame([data])
        df = df[self.FEATURES]
        features = df.values
        return features.flatten(), df

    def predict(self, data: dict) -> dict:
        raw_features, df = self.preprocess(data)
        X_transformed = self.preprocessor.transform(df)
        preds = self.model.predict_proba(X_transformed)
        preds = preds.reshape(1, -1)[0]
        shap_values = self.explainer.shap_values(X_transformed)
        response = self.postprocess(preds)
        return response

    def postprocess(self, preds: dict) -> dict:
        confidence = float(preds.max())
        prediction = int(preds.argmax())
        return {"prediction": prediction, "confidence": confidence}