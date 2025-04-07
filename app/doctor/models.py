# doctor/models.py
from pydantic import BaseModel, Field
from typing import Optional

class Doctor(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    tenant_id: str  # Reference to a Tenant document

    class Config:
        allow_population_by_field_name = True