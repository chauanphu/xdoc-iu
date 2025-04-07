# db/mongo.py
from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import settings

# Create a global client and database instance
client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongodb_uri)
db = client[settings.mongodb_db_name]

async def get_database():
    """
    Dependency function to retrieve the MongoDB database.
    This can be used with FastAPI's dependency injection.
    """
    return db