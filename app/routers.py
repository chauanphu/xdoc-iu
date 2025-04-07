
from fastapi import APIRouter
from patient.routes import router as patient_router
api_router = APIRouter(prefix="/api")

# Include the patient router
api_router.include_router(patient_router)