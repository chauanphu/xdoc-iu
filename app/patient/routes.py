# patient/routes.py
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from db.mongo import get_database
from auth.services import hash_password
from auth.models import RoleEnum
from .models import PatientCreate, PatientProfile, PatientBaseModel

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.get("/", response_model=list[PatientBaseModel])
async def list_patients(db: AsyncIOMotorDatabase = Depends(get_database)):
    patients = await db["patients"].find().to_list(length=100)
    if not patients:
        raise HTTPException(status_code=404, detail="No patients found")
    return patients 

@router.post("/")
async def create_patient(patient_create: PatientCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    # Hash the password before storing
    # Create the account in the database
    account_data = {
        "_id": str(uuid.uuid4()),
        "email": patient_create.email,
        "hashed_password": hash_password(patient_create.password),
        "role": RoleEnum.PATIENT,
    }
    # Save the account in the database
    account_result = await db["accounts"].insert_one(account_data)
    if not account_result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to create account")
    # Save the patient profile in the database
    patient_create.account_id = str(account_result.inserted_id)
    patient = PatientProfile(**patient_create.model_dump())
    result = await db["patients"].insert_one(patient.model_dump())
    if result.inserted_id:
        return status.HTTP_201_CREATED
    else:
        raise HTTPException(status_code=500, detail="Failed to create patient")
