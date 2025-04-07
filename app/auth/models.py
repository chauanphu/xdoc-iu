# auth/schemas.py
from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import Optional

class RoleEnum(str, Enum):
    DOCTOR = "DOCTOR"
    PATIENT = "PATIENT"

class AccountCreate(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum

class AccountOut(BaseModel):
    id: str = Field(..., alias="_id")
    email: EmailStr
    role: RoleEnum

    class Config:
        from_attributes = True
        populate_by_name = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None