"""
MediVision AI - Backend Application
FastAPI + MongoDB + JWT Authentication + AI/ML Integration
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
import time
from app.core.config import settings
from app.core.database import init_db, close_db
from app.core.redis_client import init_redis, close_redis
from app.api.v1 import (
    auth, users, patients, doctors, admin,
    analysis, chatbot, reports, appointments,
    notifications, analytics
)

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("medivision")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    logger.info("Starting MediVision AI Backend...")
    await init_db()
    await init_redis()
    logger.info("Database and Redis connected successfully")
    yield
    logger.info("Shutting down MediVision AI Backend...")
    await close_db()
    await close_redis()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Heart Disease Detection & Medical Image Analysis Platform",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add response time header and request logging."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(
        f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s"
    )
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "message": "An unexpected error occurred. Please try again later.",
        },
    )


# Static files for uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# API Routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(patients.router, prefix="/api/v1/patients", tags=["Patients"])
app.include_router(doctors.router, prefix="/api/v1/doctors", tags=["Doctors"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["AI Analysis"])
app.include_router(chatbot.router, prefix="/api/v1/chatbot", tags=["AI Chatbot"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])
app.include_router(appointments.router, prefix="/api/v1/appointments", tags=["Appointments"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["Notifications"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])


@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to MediVision AI API",
        "docs": "/api/v1/docs",
        "version": settings.APP_VERSION,
    }
