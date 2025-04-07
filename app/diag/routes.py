# app/diagnosis/routes.py
from fastapi import APIRouter, HTTPException
from ml import get_predictor
from .models import DiseaseEnum
from .schemas import DiabetesInput, CardioInput

router = APIRouter(prefix="/diagnosis", tags=["Diagnosis"])

@router.post("/predict/diabetes/{patient_id}")
async def predict_diabetes(patient_id: str, payload: DiabetesInput):
    try:
        predictor = get_predictor(DiseaseEnum.DIABETES)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    preprocessed = predictor.preprocess(payload.model_dump())
    raw_pred = predictor.predict(preprocessed)
    result = predictor.postprocess(raw_pred)
    return result

@router.post("/predict/cardiovascular/{patient_id}")
async def predict_cardiovascular(patient_id: str, payload: CardioInput):
    try:
        predictor = get_predictor(DiseaseEnum.CARDIOVASCULAR)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    preprocessed = predictor.preprocess(payload.model_dump())
    raw_pred = predictor.predict(preprocessed)
    result = predictor.postprocess(raw_pred)
    return result

@router.get("/explain/{diag_id}")
async def explain_disease(diag_id: str):
    pass

@router.get("/{diag_id}")
async def get_diag_history(diag_id: str):
    pass