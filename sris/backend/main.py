from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models.database import Base, engine
from api import auth, data, ml
import os

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from fastapi import Request

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Retail Intelligence System API")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Ultra-permissive CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(data.router, prefix="/api/data", tags=["Data Management"])
app.include_router(ml.router, prefix="/api/ml", tags=["Machine Learning"])

# Serve Frontend
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(frontend_path, "login.html"))

@app.get("/{page_name}.html")
async def serve_page(page_name: str):
    file_path = os.path.join(frontend_path, f"{page_name}.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(frontend_path, "login.html"))

@app.get("/")
def read_root():
    return {"message": "SRIS API is Online", "database_connected": True}
