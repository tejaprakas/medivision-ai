"""
Database Configuration
MongoDB connection using Motor (async) and Beanie (ODM).
"""

import logging
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.models import user, patient, doctor, analysis, report, appointment, notification

logger = logging.getLogger("medivision.db")

motor_client: AsyncIOMotorClient = None


async def init_db():
    """Initialize MongoDB connection and Beanie ODM."""
    global motor_client
    motor_client = AsyncIOMotorClient(
        settings.MODB
    )
    database = motor_client.get_database()

    await init_beanie(
        database=database,
        document_models=[
            user.User,
            patient.PatientProfile,
            doctor.DoctorProfile,
            analysis.AnalysisResult,
            report.MedicalReport,
            appointment.Appointment,
            notification.Notification,
        ],
    )
    logger.info("MongoDB connected and Beanie initialized")


async def close_db():
    """Close MongoDB connection."""
    global motor_client
    if motor_client:
        motor_client.close()
        logger.info("MongoDB connection closed")


def get_database():
    """Get MongoDB database instance."""
    if motor_client is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return motor_client.get_database()
