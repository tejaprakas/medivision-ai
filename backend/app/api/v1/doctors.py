"""
Doctor API Routes
Doctor profiles, availability, and patient management.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.security import get_current_user, require_doctor
from app.core.database import get_database
from app.models.user import User
from app.models.doctor import DoctorProfile, DoctorProfileUpdate, DoctorProfileResponse
import logging

logger = logging.getLogger("medivision.doctors")
router = APIRouter()


@router.get("/list", response_model=list[DoctorProfileResponse])
async def list_doctors(
    specialization: str = Query(None),
    available_only: bool = Query(True),
    current_user: User = Depends(get_current_user),
):
    """List all available doctors."""
    db = get_database()
    query = {}
    if specialization:
        query["specialization"] = {"$regex": specialization, "$options": "i"}
    if available_only:
        query["is_available"] = True

    cursor = db.doctor_profiles.find(query)
    doctors = []
    async for doc in cursor:
        user = await db.users.find_one({"_id": doc["user_id"]})
        doctors.append(DoctorProfileResponse(
            id=str(doc["_id"]),
            user_id=doc["user_id"],
            full_name=user.get("full_name", "") if user else "",
            email=user.get("email", "") if user else "",
            qualification=doc.get("qualification"),
            specialization=doc.get("specialization"),
            license_number=doc.get("license_number"),
            hospital=doc.get("hospital"),
            experience_years=doc.get("experience_years"),
            consultation_fee=doc.get("consultation_fee"),
            about=doc.get("about"),
            available_days=doc.get("available_days", []),
            rating=doc.get("rating", 0),
            total_reviews=doc.get("total_reviews", 0),
            total_patients=doc.get("total_patients", 0),
            is_available=doc.get("is_available", True),
        ))
    return doctors


@router.get("/profile", response_model=DoctorProfileResponse)
async def get_doctor_profile(current_user: User = Depends(require_doctor)):
    """Get current doctor's profile."""
    db = get_database()
    doc = await db.doctor_profiles.find_one({"user_id": str(current_user.id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor profile not found")

    return DoctorProfileResponse(
        id=str(doc["_id"]),
        user_id=doc["user_id"],
        full_name=current_user.full_name,
        email=current_user.email,
        qualification=doc.get("qualification"),
        specialization=doc.get("specialization"),
        license_number=doc.get("license_number"),
        hospital=doc.get("hospital"),
        experience_years=doc.get("experience_years"),
        consultation_fee=doc.get("consultation_fee"),
        about=doc.get("about"),
        available_days=doc.get("available_days", []),
        rating=doc.get("rating", 0),
        total_reviews=doc.get("total_reviews", 0),
        total_patients=doc.get("total_patients", 0),
        is_available=doc.get("is_available", True),
    )


@router.put("/profile")
async def update_doctor_profile(
    data: DoctorProfileUpdate,
    current_user: User = Depends(require_doctor),
):
    """Update doctor profile."""
    db = get_database()
    update_data = {k: v for k, v in data.dict().items() if v is not None}

    if update_data:
        await db.doctor_profiles.update_one(
            {"user_id": str(current_user.id)},
            {"$set": update_data},
        )

    return {"message": "Profile updated successfully"}
