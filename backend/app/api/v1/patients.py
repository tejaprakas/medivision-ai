"""
Patient API Routes
Patient profiles and medical history management.
"""

from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user, require_patient
from app.core.database import get_database
from app.models.user import User
from app.models.patient import PatientProfile, PatientProfileUpdate, PatientProfileResponse
import logging

logger = logging.getLogger("medivision.patients")
router = APIRouter()


@router.get("/profile", response_model=PatientProfileResponse)
async def get_patient_profile(current_user: User = Depends(require_patient)):
    """Get current patient's profile."""
    db = get_database()
    doc = await db.patient_profiles.find_one({"user_id": str(current_user.id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Patient profile not found")

    return PatientProfileResponse(
        id=str(doc["_id"]),
        user_id=doc["user_id"],
        age=doc.get("age"),
        gender=doc.get("gender"),
        blood_group=doc.get("blood_group"),
        height_cm=doc.get("height_cm"),
        weight_kg=doc.get("weight_kg"),
        address=doc.get("address"),
        city=doc.get("city"),
        state=doc.get("state"),
        country=doc.get("country", "India"),
        health_score=doc.get("health_score"),
        total_analyses=doc.get("total_analyses", 0),
        total_reports=doc.get("total_reports", 0),
        created_at=doc.get("created_at"),
    )


@router.put("/profile")
async def update_patient_profile(
    data: PatientProfileUpdate,
    current_user: User = Depends(require_patient),
):
    """Update patient profile."""
    db = get_database()
    update_data = {k: v for k, v in data.dict().items() if v is not None}

    if update_data:
        await db.patient_profiles.update_one(
            {"user_id": str(current_user.id)},
            {"$set": update_data},
        )

    return {"message": "Profile updated successfully"}
