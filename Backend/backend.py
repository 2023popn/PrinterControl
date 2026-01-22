"""
Bare Minimum FastAPI Backend
This is the absolute simplest FastAPI setup that connects to a frontend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ============= SETUP =============

app = FastAPI()

# CORS - Allow Streamlit to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= SCHEMAS =============

class Message(BaseModel):
    text: str

# ============= ENDPOINTS =============

@app.get("/")
def root():
    """Health check endpoint"""
    return {"status": "Backend is running!"}

@app.get("/api/data")
def get_data():
    """Example GET endpoint"""
    return {
        "message": "Hello from backend!",
        "count": 42
    }

@app.post("/api/data")
def post_data(msg: Message):
    """Example POST endpoint"""
    return {
        "received": msg.text,
        "processed": msg.text.upper()
    }

# ============= RUN =============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)