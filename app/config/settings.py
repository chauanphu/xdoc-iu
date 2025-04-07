# config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "xdoc_db"

    class Config:
        env_file = ".env"  # Optional: load environment variables from a file

settings = Settings()
