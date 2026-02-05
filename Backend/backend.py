"""
Bare Minimum FastAPI Backend
This is the absolute simplest FastAPI setup that connects to a frontend
"""
# API import statements
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Printing import statements
from printer import *

# File managing import statements
from fileManager import *

# Generic import statements
from typing import List, Optional

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

# ============= Printers =============

printers: List[Printer] = []

# ============= SCHEMAS =============

class Message(BaseModel):
    text: str

class PrinterConfig(BaseModel):
    """Configuration for a new printer"""
    port: str = '/dev/ttyUSB0'
    baud: int = 115200
    connection_timeout: int = 10
    name: Optional[str] = None  # Optional friendly name

# ============= ENDPOINTS =============

# ====== Testing Endpoints ======

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

@app.post("/api/data")
def post_data(msg: Message):
    """Example POST endpoint"""
    return {
        "received": msg.text,
        "processed": msg.text.upper()
    }

# ====== Printing Endpoints ======


@app.post("/printers/add")
async def add_printer(config: PrinterConfig):
    """Create a new printer instance and add it to the list"""
    try:
        # Create new printer object
        new_printer = Printer(
            port=config.port,
            baud=config.baud,
            connection_timeout=config.connection_timeout,
            name=config.name
        )

        # Add to list and assign ID
        new_printer.printer_id = len(printers)
        printers.append(new_printer)

        return {
            "status": "created",
            "printer_id": new_printer.printer_id,
            "printer_name": new_printer.name,
            "total_printers": len(printers)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/printers")
async def list_printers():
    """List all printer instances"""
    return {
        "printers": printers,
        "total": len(printers)
    }


@app.get("/printers/{printer_id}")
async def get_printer_status(printer_id: int):
    """Get status of a specific printer"""
    if printer_id >= len(printers) or printer_id < 0:
        raise HTTPException(status_code=404, detail="Printer not found")

    return printers[printer_id].get_status()


@app.post("/printers/{printer_id}/queue/add")
async def add_to_printer_queue(printer_id: int, filepath: str):
    """Add a file to a specific printer's queue"""
    if printer_id >= len(printers) or printer_id < 0:
        raise HTTPException(status_code=404, detail="Printer not found")

    try:
        await printers[printer_id].add_to_queue(filepath)
        return {
            "status": "added",
            "printer_id": printer_id,
            "queue_length": len(printers[printer_id].queue)
        }
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.delete("/printers/{printer_id}")
async def remove_printer(printer_id: int):
    """Remove a printer from the list"""
    if printer_id >= len(printers) or printer_id < 0:
        raise HTTPException(status_code=404, detail="Printer not found")

    # Disconnect before removing
    printers[printer_id].disconnect_printer()
    removed_printer = printers.pop(printer_id)

    # Update IDs for remaining printers
    for i, printer in enumerate(printers):
        printer.printer_id = i

    return {
        "status": "removed",
        "printer_name": removed_printer.name
    }

# ============= RUN =============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)