# app/schemas.py
from pydantic import BaseModel

class DiabetesInput(BaseModel):
    glucose: float
    bmi: float
    age: int

class CardioInput(BaseModel):
    systolic_bp: float
    diastolic_bp: float
    cholesterol: float
    age: int