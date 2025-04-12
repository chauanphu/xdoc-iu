# auth/routes.py
import uuid
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from auth.models import AccountCreate, AccountOut, Token
from auth.services import (
    hash_password,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from db.mongo import get_database

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=AccountOut)
async def register(account: AccountCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    # Check if email already exists
    existing = await db["accounts"].find_one({"email": account.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    account_data = {
        "_id": str(uuid.uuid4()),
        "email": account.email,
        "hashed_password": hash_password(account.password),
        "role": account.role,
    }
    await db["accounts"].insert_one(account_data)
    return account_data

@router.post("/login", response_model=Token)
async def login(account: AccountCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    user = await db["accounts"].find_one({"email": account.email})
    if not user or not verify_password(account.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"], "role": user["role"]},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}