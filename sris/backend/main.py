from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models.database import Base, engine
from api import auth, data, ml
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Retail Intelligence System API")

# Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response

# CORS
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

# Mount CSS and JS folders for the browser to find them
if os.path.exists(os.path.join(frontend_path, "css")):
    app.mount("/css", StaticFiles(directory=os.path.join(frontend_path, "css")), name="css")
if os.path.exists(os.path.join(frontend_path, "js")):
    app.mount("/js", StaticFiles(directory=os.path.join(frontend_path, "js")), name="js")

# Health Check
@app.get("/health")
def health_check():
    return {"status": "online", "database": "connected"}

# Serve HTML Pages (Catch-all for frontend)
@app.get("/{page_name}.html")
async def serve_html_pages(page_name: str):
    file_path = os.path.join(frontend_path, f"{page_name}.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(frontend_path, "login.html"))

# Root Redirect - MUST BE LAST
@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(frontend_path, "login.html"))
