# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model import load_model, predict
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(title="MaaS REST API")

# Load model at startup
model = load_model()

# Define a request body schema using Pydantic
class PredictionRequest(BaseModel):
    feature1: float
    feature2: float
    # add other features as needed

# Define an endpoint for predictions
@app.post("/predict")
def get_prediction(request: PredictionRequest):
    try:
        # Convert incoming data into a format for your model
        input_data = request.dict()
        # Get prediction from your model
        result = predict(model, input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health-check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}

origins = [FRONTEND_ENDPOINT]
origins.append("http://localhost:5173")

if DEBUG:
    origins.extend(["http://localhost:3000", "http://localhost:8000", "http://localhost:8080", "http://localhost:80", "http://localhost:5173"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

if __name__ == "main":
