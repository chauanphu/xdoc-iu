# config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "xdoc_db"
    jwt_secret_key: str = "your_jwt_secret_key"
    jwt_access_token_expires_minutes: int = 30  # Token expiration time in minutes
    GEMINI_API_KEY: str
    class Config:
        env_file = ".env"  # Optional: load environment variables from a file

settings = Settings()