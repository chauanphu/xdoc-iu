
from fastapi import APIRouter
from patient.routes import router as patient_router
from auth.routes import router as auth_router
from diag.routes import router as diag_router

api_router = APIRouter(prefix="/api")

api_router.include_router(patient_router)
api_router.include_router(auth_router)
api_router.include_router(diag_router)