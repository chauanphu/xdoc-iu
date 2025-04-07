# tenant/models.py
from pydantic import BaseModel, Field
from typing import Optional

class Hospital(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    product_key: str

    class Config:
        validate_by_name = True