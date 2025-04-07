# app/ml/model.py
import xgboost as xgb
import numpy as np
from abc import ABC, abstractmethod
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import os

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
        features_scaled = self.scaler.transform(df)
        return features_scaled

    def predict(self, preprocessed_data: np.ndarray) -> dict:
        preds = self.model.predict_proba(preprocessed_data)
        return {"raw_prediction": preds}

    def postprocess(self, raw_prediction: dict) -> dict:
        preds = raw_prediction["raw_prediction"]
        confidence = float(preds.max())
        prediction = int(preds.argmax())
        return {"prediction": prediction, "confidence": confidence}
    
    def load(self, model_path: str, scaler_path: str = None):
        """Load model and scaler"""
        # Load the model
        self.model.load_model(model_path)
        
        # Load the scaler if path is provided and file exists
        if scaler_path and os.path.exists(scaler_path):
            self.scaler = joblib.load(scaler_path)

class CardioPredictor(DiseasePredictor):
    def __init__(self, model_path: str):
        self.model = xgb.Booster()
        self.model.load_model(model_path)
    
    def preprocess(self, data: dict) -> np.ndarray:
        # Extract diabetes-specific features
        features = np.array([data[k] for k in sorted(data.keys()) if k in ["glucose", "bmi", "age"]])
        return features.reshape(1, -1)

    def predict(self, preprocessed_data: np.ndarray) -> dict:
        dmatrix = xgb.DMatrix(preprocessed_data)
        preds = self.model.predict(dmatrix)
        return {"raw_prediction": preds}

    def postprocess(self, raw_prediction: dict) -> dict:
        preds = raw_prediction["raw_prediction"]
        confidence = float(preds.max())
        prediction = int(preds.argmax())
        return {"prediction": prediction, "confidence": confidence}