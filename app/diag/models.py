# diagnosis/models.py
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class DiseaseEnum(str, Enum):
    DIABETES = "diabetes"
    CARDIOVASCULAR = "cardiovascular"
    # Add other diseases as needed
    
class Diagnosis(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    patient_id: str       # Reference to a PatientProfile document
    doctor_id: Optional[str] = None  # Reference to a Doctor document; can be null for self-diagnosis
    time: datetime = Field(default_factory=datetime.utcnow)
    prediction: str
    conf: float           # Confidence between 0 and 1
    explain: str          # Natural language explanation

    class Config:
        validate_by_name = True