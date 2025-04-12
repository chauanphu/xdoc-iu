# doctor/services.py
from motor.motor_asyncio import AsyncIOMotorDatabase
from .models import Doctor, DoctorCreate
from typing import List, Optional
from bson import ObjectId

async def get_doctor_by_id(db: AsyncIOMotorDatabase, doctor_id: str) -> Optional[Doctor]:
    """
    Retrieve a doctor by ID
    """
    doctor_data = await db["doctors"].find_one({"_id": doctor_id})
    if doctor_data:
        return Doctor(**doctor_data)
    return None

async def get_doctor_by_account_id(db: AsyncIOMotorDatabase, account_id: str) -> Optional[Doctor]:
    """
    Retrieve a doctor by their account ID
    """
    doctor_data = await db["doctors"].find_one({"account_id": account_id})
    if doctor_data:
        return Doctor(**doctor_data)
    return None

async def get_doctors_by_tenant(db: AsyncIOMotorDatabase, tenant_id: str) -> List[Doctor]:
    """
    Retrieve all doctors for a specific tenant/hospital
    """
    doctors = await db["doctors"].find({"tenant_id": tenant_id}).to_list(length=100)
    return [Doctor(**doc) for doc in doctors]

async def create_doctor(db: AsyncIOMotorDatabase, doctor_data: DoctorCreate, account_id: str) -> Doctor:
    """
    Create a new doctor associated with a tenant/hospital
    """
    # Prepare doctor document
    doctor_dict = doctor_data.dict(exclude={"password", "email"})
    doctor_dict["account_id"] = account_id
    
    # Ensure the doctor is linked to a tenant
    if "tenant_id" not in doctor_dict or not doctor_dict["tenant_id"]:
        raise ValueError("A doctor must be associated with a tenant (hospital)")
    
    # Insert into the database
    result = await db["doctors"].insert_one(doctor_dict)
    doctor_dict["_id"] = result.inserted_id
    
    return Doctor(**doctor_dict)

async def update_doctor(db: AsyncIOMotorDatabase, doctor_id: str, updated_data: dict) -> bool:
    """
    Update a doctor's information
    """
    # Don't allow updates to account_id or tenant_id for security
    if "account_id" in updated_data:
        updated_data.pop("account_id")
    if "tenant_id" in updated_data:
        updated_data.pop("tenant_id")
        
    result = await db["doctors"].update_one(
        {"_id": doctor_id},
        {"$set": updated_data}
    )
    return result.modified_count > 0

async def delete_doctor(db: AsyncIOMotorDatabase, doctor_id: str, tenant_id: str) -> bool:
    """
    Delete a doctor, ensuring they belong to the specified tenant
    """
    # Only delete if the doctor belongs to the specified tenant
    result = await db["doctors"].delete_one({
        "_id": doctor_id,
        "tenant_id": tenant_id
    })
    return result.deleted_count > 0