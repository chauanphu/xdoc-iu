# doctor/models.py
from pydantic import BaseModel, Field
from typing import Optional
import re
from bson import ObjectId

class Doctor(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    tenant_id: str  # Reference to a Tenant document
    account_id: Optional[str] = None

    class Config:
        validate_by_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        populate_by_name = True

class DoctorCreate(Doctor):
    password: str  # Password for the doctor account
    email: str  # Email for the doctor account
    
    @staticmethod
    def is_strong_password(password: str) -> bool:
        # Ensure password has at least 8 characters, one uppercase, one lowercase, one digit, and one special character
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        return bool(re.match(pattern, password))