# patient/models.py
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional

class GenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

class PatientBaseModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    dob: datetime
    gender: GenderEnum
    age: int

class PatientProfile(PatientBaseModel):
    tenant_id: Optional[str] = None  # Patient may be standalone or assigned to a tenant
    account_id: str = None

    class Config:
        allow_population_by_field_name = True

class PatientCreate(PatientProfile):
    password: str  # Password for the patient, if applicable
    email: str  # Email for the patient, if applicable

    class Config:
        allow_population_by_field_name = True