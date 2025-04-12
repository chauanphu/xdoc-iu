# config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "xdoc_db"
    jwt_secret_key: str = "your_jwt_secret_key"
    jwt_access_token_expires_minutes: int = 30  # Token expiration time in minutes
    GEMINI_API_KEY: str
    
    # Multi-tenant settings
    # If True, will create separate databases for each tenant
    use_tenant_databases: bool = False
    # If True, will create collections with tenant prefixes
    use_tenant_collections: bool = False
    # Default tenant ID for single-tenant mode or system-wide operations
    default_tenant_id: str = "default"
    
    class Config:
        env_file = ".env"  # Optional: load environment variables from a file

settings = Settings()