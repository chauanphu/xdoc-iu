# hospital/services.py
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient
from .models import Hospital
from typing import List, Optional
from bson import ObjectId
from app.config.settings import settings

async def get_hospital_by_id(db: AsyncIOMotorDatabase, hospital_id: str) -> Optional[Hospital]:
    """
    Retrieve a hospital/tenant by ID
    """
    if isinstance(hospital_id, str) and len(hospital_id) == 24:
        try:
            hospital_id_obj = ObjectId(hospital_id)
            hospital_data = await db["hospitals"].find_one({"_id": hospital_id_obj})
            if hospital_data:
                return Hospital(**hospital_data)
        except:
            pass
    return None

async def get_hospital_by_product_key(db: AsyncIOMotorDatabase, product_key: str) -> Optional[Hospital]:
    """
    Retrieve a hospital/tenant by product key
    """
    hospital_data = await db["hospitals"].find_one({"product_key": product_key})
    if hospital_data:
        return Hospital(**hospital_data)
    return None

async def create_hospital(db: AsyncIOMotorDatabase, name: str, product_key: str) -> Hospital:
    """
    Create a new hospital/tenant
    """
    hospital_data = {
        "name": name,
        "product_key": product_key
    }
    
    result = await db["hospitals"].insert_one(hospital_data)
    hospital_data["_id"] = result.inserted_id
    return Hospital(**hospital_data)

async def get_all_hospitals(db: AsyncIOMotorDatabase) -> List[Hospital]:
    """
    Retrieve all hospitals/tenants
    """
    hospitals = await db["hospitals"].find().to_list(length=100)
    return [Hospital(**hosp) for hosp in hospitals]

async def update_hospital(db: AsyncIOMotorDatabase, hospital_id: str, updated_data: dict) -> bool:
    """
    Update hospital/tenant information
    """
    if isinstance(hospital_id, str) and len(hospital_id) == 24:
        try:
            hospital_id_obj = ObjectId(hospital_id)
            result = await db["hospitals"].update_one(
                {"_id": hospital_id_obj},
                {"$set": updated_data}
            )
            return result.modified_count > 0
        except:
            pass
    return False

async def get_tenant_db(tenant_id: str) -> AsyncIOMotorDatabase:
    """
    Get a database instance for a specific tenant
    
    This enables true database-level multi-tenancy where each tenant has its own
    database. For shared database/collection approach, simply use the tenant_id
    field in queries.
    """
    # client = AsyncIOMotorClient(settings.mongodb_uri)
    # return client[f"{settings.mongodb_db_name}_{tenant_id}"]
    
    # Using the main database
    client = AsyncIOMotorClient(settings.mongodb_uri)
    return client[settings.mongodb_db_name]