# patient/services.py
from motor.motor_asyncio import AsyncIOMotorDatabase
from .models import PatientProfile, PatientCreate
from typing import List, Optional
from bson import ObjectId
from utils.encryption import encrypt_dict_fields, decrypt_dict_fields

# Fields that should be encrypted in the patient profile
ENCRYPTED_FIELDS = ["name", "dob"]

async def get_patient_by_id(db: AsyncIOMotorDatabase, patient_id: str, tenant_id: Optional[str] = None) -> Optional[PatientProfile]:
    """
    Retrieve a patient by ID, optionally filtering by tenant
    """
    query = {"_id": ObjectId(patient_id) if isinstance(patient_id, str) else patient_id}
    if tenant_id:
        query["tenant_id"] = tenant_id
        
    patient_data = await db["patients"].find_one(query)
    if patient_data:
        # Decrypt sensitive fields before returning
        decrypted_data = decrypt_dict_fields(patient_data, ENCRYPTED_FIELDS)
        return PatientProfile(**decrypted_data)
    return None

async def get_patient_by_account_id(db: AsyncIOMotorDatabase, account_id: str) -> Optional[PatientProfile]:
    """
    Retrieve a patient by their account ID
    """
    patient_data = await db["patients"].find_one({"account_id": account_id})
    if patient_data:
        # Decrypt sensitive fields before returning
        decrypted_data = decrypt_dict_fields(patient_data, ENCRYPTED_FIELDS)
        return PatientProfile(**decrypted_data)
    return None

async def get_patients_by_tenant(db: AsyncIOMotorDatabase, tenant_id: str) -> List[PatientProfile]:
    """
    Retrieve all patients for a specific tenant/hospital
    """
    patients = await db["patients"].find({"tenant_id": tenant_id}).to_list(length=100)
    # Decrypt each patient's sensitive data
    decrypted_patients = [decrypt_dict_fields(patient, ENCRYPTED_FIELDS) for patient in patients]
    return [PatientProfile(**patient) for patient in decrypted_patients]

async def create_patient(db: AsyncIOMotorDatabase, patient_data: PatientCreate, account_id: str) -> PatientProfile:
    """
    Create a new patient, optionally associating with a tenant/hospital
    """
    # Prepare patient document
    # Use model_dump() instead of dict() for Pydantic v2 compatibility
    patient_dict = patient_data.model_dump(exclude={"password", "email"})
    patient_dict["account_id"] = account_id
    
    # Encrypt sensitive fields before storing
    encrypted_dict = encrypt_dict_fields(patient_dict, ENCRYPTED_FIELDS)
    
    # Insert into the database
    result = await db["patients"].insert_one(encrypted_dict)
    patient_dict["_id"] = result.inserted_id
    
    return PatientProfile(**patient_dict)

async def update_patient(db: AsyncIOMotorDatabase, patient_id: str, updated_data: dict, tenant_id: Optional[str] = None) -> bool:
    """
    Update a patient's information, optionally ensuring they belong to a specific tenant
    """
    # Don't allow updates to account_id for security
    if "account_id" in updated_data:
        updated_data.pop("account_id")
    
    # Encrypt any sensitive fields in the update
    encrypted_update = encrypt_dict_fields(updated_data, ENCRYPTED_FIELDS)
    
    # Build query
    query = {"_id": ObjectId(patient_id) if isinstance(patient_id, str) else patient_id}
    if tenant_id:
        # Only update if the patient belongs to the specified tenant
        query["tenant_id"] = tenant_id
        
    result = await db["patients"].update_one(
        query,
        {"$set": encrypted_update}
    )
    return result.modified_count > 0

async def delete_patient(db: AsyncIOMotorDatabase, patient_id: str, tenant_id: Optional[str] = None) -> bool:
    """
    Delete a patient, optionally ensuring they belong to the specified tenant
    """
    # Build query
    query = {"_id": ObjectId(patient_id) if isinstance(patient_id, str) else patient_id}
    if tenant_id:
        # Only delete if the patient belongs to the specified tenant
        query["tenant_id"] = tenant_id
    
    result = await db["patients"].delete_one(query)
    return result.deleted_count > 0

async def assign_patient_to_tenant(db: AsyncIOMotorDatabase, patient_id: str, tenant_id: str) -> bool:
    """
    Assign a patient to a specific tenant/hospital
    """
    result = await db["patients"].update_one(
        {"_id": ObjectId(patient_id) if isinstance(patient_id, str) else patient_id},
        {"$set": {"tenant_id": tenant_id}}
    )
    return result.modified_count > 0