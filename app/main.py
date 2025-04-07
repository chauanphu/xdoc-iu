# app.py
from fastapi import FastAPI, HTTPException

# Initialize FastAPI app
app = FastAPI(title="XDoc REST API")

# Health-check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}