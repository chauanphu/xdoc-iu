# doctor/routes.py
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from db.mongo import get_database
from auth.services import hash_password
from auth.models import RoleEnum
from .models import Doctor, DoctorCreate

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.get("/", response_model=list[Doctor])
async def list_doctors(db: AsyncIOMotorDatabase = Depends(get_database)):
    doctors = await db["doctors"].find().to_list(length=100)
    if not doctors:
        raise HTTPException(status_code=404, detail="No doctors found")
    return doctors

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_doctor(doctor_create: DoctorCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    # Validate password strength
    if not DoctorCreate.is_strong_password(doctor_create.password):
        raise HTTPException(status_code=400, detail="Weak password")
    
    # Check if email is already used
    existing_account = await db["accounts"].find_one({"email": doctor_create.email})
    if existing_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create the account in the database
    account_id = str(uuid.uuid4())
    account_data = {
        "_id": account_id,
        "email": doctor_create.email,
        "hashed_password": hash_password(doctor_create.password),
        "role": RoleEnum.DOCTOR,
    }
    
    # Save the account in the database
    account_result = await db["accounts"].insert_one(account_data)
    if not account_result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to create account")
    
    # Save the doctor profile in the database
    doctor_data = doctor_create.model_dump()
    doctor_data["account_id"] = account_id
    
    # Remove password as we don't want to store it in the doctor collection
    doctor_data.pop("password", None)
    
    result = await db["doctors"].insert_one(doctor_data)
    if not result.inserted_id:
        # Rollback the account creation if doctor profile creation fails
        await db["accounts"].delete_one({"_id": account_id})
        raise HTTPException(status_code=500, detail="Failed to create doctor")
    
    return {"message": "Doctor created successfully", "doctor_id": str(result.inserted_id)}

@router.get("/{doctor_id}", response_model=Doctor)
async def get_doctor(doctor_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    doctor = await db["doctors"].find_one({"_id": doctor_id})
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor