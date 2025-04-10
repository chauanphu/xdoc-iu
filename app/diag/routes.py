# app/diagnosis/routes.py
from fastapi import APIRouter, Depends, HTTPException
from auth.services import get_current_user
from ml import get_predictor
from .models import DiseaseEnum, DiabetesInput, CardioInput
from db.mongo import get_database
router = APIRouter(prefix="/diagnosis", tags=["Diagnosis"])

#############################
# For Doctor
#############################

@router.post("/predict/diabetes/{patient_id}")
async def predict_diabetes(patient_id: str, payload: DiabetesInput, db=Depends(get_database)):
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

###############################
# For Patient
###############################
@router.post("/predict/diabetes/")
async def predict_diabetes(payload: DiabetesInput):
    try:
        predictor = get_predictor(DiseaseEnum.DIABETES)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    result = predictor.predict(payload.model_dump())
    return result

@router.post("/predict/cardiovascular/")
async def predict_cardiovascular(payload: CardioInput):
    try:
        predictor = get_predictor(DiseaseEnum.CARDIOVASCULAR)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    if not predictor:
        raise HTTPException(status_code=500, detail="Model not found")
    
    response = predictor.predict(payload.model_dump())
    return response

@router.get("/explain/{diag_id}")
async def explain_disease(diag_id: str, level: int = 0):
    pass

@router.get("/")
async def get_diag_history(diag_id: str):
    pass

@router.get("/{patient_id}")
async def get_patient_history(patient_id: str):
    pass