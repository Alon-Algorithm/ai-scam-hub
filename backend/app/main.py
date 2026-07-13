from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from contextlib import asynccontextmanager
import logging
from typing import Optional

from app.api import auth, scam_detection, job_checker, url_safety, image_analysis, misinformation
from app.core.database import engine, SessionLocal
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting AI Misinformation & Scam Hub...")
    yield
    # Shutdown
    logger.info("Shutting down...")

app = FastAPI(
    title="AI Misinformation & Scam Hub",
    description="AI-powered scam detection and misinformation analysis platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(scam_detection.router, prefix="/api/scam", tags=["Scam Detection"])
app.include_router(job_checker.router, prefix="/api/jobs", tags=["Job Analysis"])
app.include_router(url_safety.router, prefix="/api/url", tags=["URL Safety"])
app.include_router(image_analysis.router, prefix="/api/image", tags=["Image Analysis"])
app.include_router(misinformation.router, prefix="/api/misinfo", tags=["Misinformation"])

@app.get("/")
async def root():
    return {
        "message": "AI Misinformation & Scam Hub API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}