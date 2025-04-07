# app/ml/preprocess.py
import numpy as np

def preprocess(data: dict) -> np.ndarray:
    # Implement data transformation and validation
    return np.array([data[key] for key in sorted(data.keys())])

# app/ml/postprocess.py
def postprocess(preds: np.ndarray) -> dict:
    # For instance, include prediction confidence or thresholding logic
    confidence = float(preds.max())
    prediction = int(preds.argmax())
    return {"prediction": prediction, "confidence": confidence}