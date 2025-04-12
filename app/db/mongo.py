# db/mongo.py
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config.settings import settings
from hospital.context import get_current_tenant_id
from typing import Optional

# Create a global client instance
print("Connecting to MongoDB...: ", settings.MONGO_URI)
client: AsyncIOMotorClient = AsyncIOMotorClient(settings.MONGO_URI)
async def get_database() -> AsyncIOMotorDatabase:
    """
    Dependency function to retrieve the MongoDB database.
    If tenant context is set, it will use tenant-specific collections.
    
    This supports a multi-collection approach to multi-tenancy, where 
    each tenant's data is prefixed in collection names.
    """
    # Using a single database for all tenants
    db = client[settings.MONGO_DB_NAME]
    return db

async def get_tenant_database(tenant_id: Optional[str] = None) -> AsyncIOMotorDatabase:
    """
    Get a database for a specific tenant.
    If tenant_id is not provided, uses the current tenant context.
    
    This supports a multi-database approach where each tenant gets its own database.
    """
    # If no tenant ID provided, try to get from context
    if not tenant_id:
        tenant_id = get_current_tenant_id()
    
    # If we have a tenant ID and want multi-db, return tenant-specific database
    if tenant_id and settings.use_tenant_databases:
        return client[f"{settings.mongodb_db_name}_{tenant_id}"]
    
    # Otherwise return the default database
    return client[settings.mongodb_db_name]

def get_tenant_collection_name(base_collection: str, tenant_id: Optional[str] = None) -> str:
    """
    Get a collection name for a specific tenant.
    If tenant_id is not provided, uses the current tenant context.
    
    This supports a multi-collection approach where each tenant's collections have a prefix.
    """
    # If no tenant ID provided, try to get from context
    if not tenant_id:
        tenant_id = get_current_tenant_id()
    
    # If we have a tenant ID and want multi-collection, return prefixed collection name
    if tenant_id and settings.use_tenant_collections:
        return f"{tenant_id}_{base_collection}"
    
    # Otherwise return the base collection name
    return base_collection