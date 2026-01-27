"""
Bare Minimum FastAPI Backend
This is the absolute simplest FastAPI setup that connects to a frontend
"""
# API import statements
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Printing import statements
from printrun.printcore import printcore
from printrun import gcoder
import time

# File managing import statements
from fileManager import *

# Printing import statements
from printer import loadNextFileToPrint, printNextFileToPrint

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

#printer1 = printcore('COM3', 115200)

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
    currentQueueSize = get_queue_size()
    return {
        "message": "Hello from backend!",
        "count": currentQueueSize
    }

@app.get("/api/next")
def get_next():
    nextFile = get_next_file_in_queue()
    loadNextFileToPrint(nextFile)
    return {
        "file": nextFile
    }

@app.get("/api/queue")
def get_queue():
    queue = get_full_queue()
    return {
        "queue": queue
    }

@app.get("/api/print")
def print_next():
    success = printNextFileToPrint()
    return {
        "printCommunicationSuccessful" : success
    }

@app.post("/api/data")
def post_data(msg: Message):
    """Example POST endpoint"""
    return {
        "received": msg.text,
        "processed": msg.text.upper()
    }

@app.post("/api/file")
def post_file(file: UploadFile):
    """POST endpoint to recieve a file"""
    add_to_queue(file)
    return {
        "received": file.filename,
        "processed": file.filename.upper()
    }

# ============= RUN =============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)