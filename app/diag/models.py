# diagnosis/models.py
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any, Union, List

class DiseaseEnum(str, Enum):
    DIABETES = "diabetes"
    CARDIOVASCULAR = "cardiovascular"
    # Add other diseases as needed
    
class DiabetesInput(BaseModel):
    # Diabetes-specific input features
    BMI: float
    AGE: int
    Urea: Optional[float] = None
    Cr: Optional[float] = None
    HbA1c: Optional[float] = None
    Chol: Optional[float] = None
    TG: Optional[float] = None
    HDL: Optional[float] = None
    LDL: Optional[float] = None
    VLDL: Optional[float] = None

DIABETES_OUTPUT = {
    0: "negative",
    1: "prediabetes",
    2: "diabetes",
}

class CardioInput(BaseModel):
    # Cardiovascular-specific input features
    systolic_bp: float
    diastolic_bp: float
    cholesterol: float
    age: int

class DiagnosisBase(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    patient_id: str                   # Reference to a PatientProfile document
    doctor_id: Optional[str] = None   # Reference to a Doctor document; can be null for self-diagnosis
    diagnosis_time: datetime = Field(default_factory=datetime.utcnow)
    disease_type: DiseaseEnum         # Type of disease being diagnosed
    prediction: str                   # The diagnostic prediction (positive, negative, risk level, etc.)
    confidence: float = Field(..., ge=0.0, le=1.0)  # Confidence between 0 and 1
    explanation: str                  # Natural language explanation
    input_features: Dict[str, Any]    # Store the input features as a dictionary
    details: Optional[Dict[str, Any]] = None  # Optional additional details about the diagnosis

    class Config:
        validate_assignment = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class DiagnosisCreate(DiagnosisBase):
    pass

class DiagnosisOut(DiagnosisBase):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }