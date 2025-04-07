# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# from model import load_model, predict
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routers import api_router

# Initialize FastAPI app
app = FastAPI(title="XDoc REST API")
app.include_router(api_router)

origins = []
origins.append("http://localhost:5173")

# if DEBUG:
#     origins.extend(["http://localhost:3000", "http://localhost:8000", "http://localhost:8080", "http://localhost:80", "http://localhost:5173"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)