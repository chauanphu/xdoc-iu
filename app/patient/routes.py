# patient/routes.py
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from db.mongo import get_database

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.get("/")
async def list_patients(db: AsyncIOMotorDatabase = Depends(get_database)):
    patients = await db["patients"].find().to_list(length=100)
    return {"patients": patients}

@router.post("/")
async def create_patient(patient: dict, db: AsyncIOMotorDatabase = Depends(get_database)):
    result = await db["patients"].insert_one(patient)
    if result.inserted_id:
        return {"message": "Patient created", "id": str(result.inserted_id)}
    raise HTTPException(status_code=500, detail="Failed to create patient")
