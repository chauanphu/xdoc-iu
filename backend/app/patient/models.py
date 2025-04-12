# patient/models.py
from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional
import re

class GenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

class PatientBaseModel(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id", default=None)  
    name: str
    dob: datetime
    gender: GenderEnum
    age: int

    class Config:
        json_encoders = json_encoders = {ObjectId: str}  # Ensures ObjectId is serialized to a string
        populate_by_name = True
        validate_assignment = True
        arbitrary_types_allowed=True

class PatientProfile(PatientBaseModel):
    tenant_id: Optional[str]
    account_id: str = None

    class Config:
        validate_by_name = True
        arbitrary_types_allowed=True

class PatientCreate(BaseModel):
    name: str
    dob: datetime
    gender: GenderEnum
    age: int
    password: str  # Password for the patient, if applicable
    email: str  # Email for the patient, if applicable
    tenant_id: Optional[str] = None  # Optional tenant ID for multi-tenancy

    @staticmethod
    def is_strong_password(password: str) -> bool:
        # Ensure password has at least 8 characters, one uppercase, one lowercase, one digit, and one special character
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        return bool(re.match(pattern, password))