# patient/routes.py
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Path
from motor.motor_asyncio import AsyncIOMotorDatabase
from db.mongo import get_database
from auth.services import hash_password, get_current_user, require_role
from auth.models import RoleEnum, TokenData
from .models import PatientCreate, PatientProfile, PatientBaseModel
from .services import (
    get_patients_by_tenant, 
    get_patient_by_id,
    create_patient,
    update_patient,
    delete_patient
)

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.get("/", response_model=list[PatientBaseModel])
async def list_patients(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: TokenData = Depends(require_role(RoleEnum.DOCTOR))
):
    """
    List all patients - Only available to users with DOCTOR role
    """
    patients = await db["patients"].find().to_list(length=100)
    if not patients:
        raise HTTPException(status_code=404, detail="No patients found")
    return patients 

@router.get("/{patient_id}", response_model=PatientBaseModel)
async def get_patient(
    patient_id: str = Path(..., title="The ID of the patient to get"),
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: TokenData = Depends(require_role(RoleEnum.DOCTOR))
):
    """
    Get a specific patient by ID - Only available to users with DOCTOR role
    """
    patient = await get_patient_by_id(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_patient_endpoint(
    patient_create: PatientCreate, 
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Create a new patient profile with an associated account
    """
    # Hash the password before storing
    if not PatientCreate.is_strong_password(patient_create.password):
        raise HTTPException(status_code=400, detail="Weak password")
    
    account_data = {
        "_id": str(uuid.uuid4()),
        "email": patient_create.email,
        "hashed_password": hash_password(patient_create.password),
        "role": RoleEnum.PATIENT.value,  # Use .value to get the string value
    }
    
    # Create the patient using the service function which handles encryption
    try:
        # Save the account in the database
        account_result = await db["accounts"].insert_one(account_data)
        if not account_result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to create account")
        
        # Create the patient with the account link
        patient = await create_patient(db, patient_create, str(account_result.inserted_id))
        return {"id": str(patient.id), "message": "Patient created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating patient: {str(e)}")
    
@router.put("/{patient_id}")
async def update_patient_endpoint(
    updated_data: dict,
    patient_id: str = Path(..., title="The ID of the patient to update"),
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: TokenData = Depends(require_role(RoleEnum.DOCTOR))
):
    """
    Update a patient's profile - Only available to users with DOCTOR role
    """
    success = await update_patient(db, patient_id, updated_data)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found or update failed")
    return {"message": "Patient updated successfully"}

@router.delete("/{patient_id}")
async def delete_patient_endpoint(
    patient_id: str = Path(..., title="The ID of the patient to delete"),
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: TokenData = Depends(require_role(RoleEnum.DOCTOR))
):
    """
    Delete a patient - Only available to users with DOCTOR role
    """
    success = await delete_patient(db, patient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found or delete failed")
    return {"message": "Patient deleted successfully"}
