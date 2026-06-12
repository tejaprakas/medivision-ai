"""
Appointment API Routes
Book, manage, and track doctor-patient appointments.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from app.core.security import get_current_user, require_patient, require_doctor
from app.core.database import get_database
from app.models.user import User
from app.models.appointment import Appointment, AppointmentCreate, AppointmentUpdate, AppointmentResponse, AppointmentStatus
import logging

logger = logging.getLogger("medivision.appointments")
router = APIRouter()


@router.post("/book", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def book_appointment(
    data: AppointmentCreate,
    current_user: User = Depends(require_patient),
):
    """Book a new appointment with a doctor."""
    db = get_database()

    # Verify doctor exists
    doctor = await db.doctor_profiles.find_one({"user_id": data.doctor_id})
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Check for conflicts
    existing = await db.appointments.find_one({
        "doctor_id": data.doctor_id,
        "appointment_date": data.appointment_date,
        "status": {"$in": ["pending", "confirmed"]},
    })
    if existing:
        raise HTTPException(status_code=409, detail="Time slot not available")

    appointment = Appointment(
        patient_id=str(current_user.id),
        doctor_id=data.doctor_id,
        appointment_date=data.appointment_date,
        duration_minutes=data.duration_minutes,
        type=data.type,
        reason=data.reason,
        notes=data.notes,
    )
    await appointment.create()

    return AppointmentResponse(
        id=str(appointment.id),
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        appointment_date=appointment.appointment_date,
        duration_minutes=appointment.duration_minutes,
        type=appointment.type.value,
        status=appointment.status.value,
        reason=appointment.reason,
        notes=appointment.notes,
        meeting_link=appointment.meeting_link,
        created_at=appointment.created_at,
    )


@router.get("/my-appointments", response_model=list[AppointmentResponse])
async def get_my_appointments(
    status_filter: str = None,
    current_user: User = Depends(get_current_user),
):
    """Get appointments for current user."""
    db = get_database()
    query = {}

    if current_user.role.value == "patient":
        query["patient_id"] = str(current_user.id)
    elif current_user.role.value == "doctor":
        query["doctor_id"] = str(current_user.id)

    if status_filter:
        query["status"] = status_filter

    cursor = db.appointments.find(query).sort("appointment_date", 1)
    appointments = []
    async for doc in cursor:
        appointments.append(AppointmentResponse(
            id=str(doc["_id"]),
            patient_id=doc["patient_id"],
            doctor_id=doc["doctor_id"],
            appointment_date=doc["appointment_date"],
            duration_minutes=doc.get("duration_minutes", 30),
            type=doc.get("type", "in_person"),
            status=doc.get("status", "pending"),
            reason=doc.get("reason"),
            notes=doc.get("notes"),
            meeting_link=doc.get("meeting_link"),
            created_at=doc.get("created_at", datetime.utcnow()),
        ))
    return appointments


@router.patch("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: str,
    data: AppointmentUpdate,
    current_user: User = Depends(get_current_user),
):
    """Update appointment status or details."""
    db = get_database()
    appointment = await db.appointments.find_one({"_id": appointment_id})

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # Check access
    if (appointment["patient_id"] != str(current_user.id) and
        appointment["doctor_id"] != str(current_user.id) and
        current_user.role.value != "admin"):
        raise HTTPException(status_code=403, detail="Access denied")

    update_data = {}
    if data.status:
        update_data["status"] = data.status.value
    if data.notes:
        update_data["notes"] = data.notes
    if data.meeting_link:
        update_data["meeting_link"] = data.meeting_link
    if data.cancellation_reason:
        update_data["cancellation_reason"] = data.cancellation_reason

    update_data["updated_at"] = datetime.utcnow()

    await db.appointments.update_one({"_id": appointment_id}, {"$set": update_data})

    updated = await db.appointments.find_one({"_id": appointment_id})
    return AppointmentResponse(
        id=str(updated["_id"]),
        patient_id=updated["patient_id"],
        doctor_id=updated["doctor_id"],
        appointment_date=updated["appointment_date"],
        duration_minutes=updated.get("duration_minutes", 30),
        type=updated.get("type", "in_person"),
        status=updated.get("status", "pending"),
        reason=updated.get("reason"),
        notes=updated.get("notes"),
        meeting_link=updated.get("meeting_link"),
        created_at=updated.get("created_at", datetime.utcnow()),
    )
