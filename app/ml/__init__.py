from .model import DiabetesPredictor, CardioPredictor

def get_predictor(disease: str):
    try:
        if disease.lower() == "diabetes":
            return DiabetesPredictor(
                model_path="pretrained/diabetes_model.json",
                scaler_path="pretrained/diabetes.scaler.pkl",
            )
        elif disease.lower() == "cardiovascular":
            return CardioPredictor(model_path="pretrained/cardio_model.json")
        else:
            raise ValueError("Unsupported disease type")
    except Exception as e:
        print(f"Error loading model: {e}")