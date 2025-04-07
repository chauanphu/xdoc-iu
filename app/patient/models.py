# patient/models.py
from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional

class GenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

class PatientBaseModel(BaseModel):
    id: Optional[ObjectId] | Optional[str] = Field(alias="_id", default=None)  
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
    tenant_id: Optional[str] = None  # Patient may be standalone or assigned to a tenant
    account_id: str = None

    class Config:
        validate_by_name = True

class PatientCreate(PatientProfile):
    password: str  # Password for the patient, if applicable
    email: str  # Email for the patient, if applicable