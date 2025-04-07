# app/ml/model.py
import xgboost as xgb
import numpy as np
from abc import ABC, abstractmethod

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