"""
Appointment Model
Stores doctor-patient appointment bookings.
"""

from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class AppointmentStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class AppointmentType(str, Enum):
    IN_PERSON = "in_person"
    VIDEO = "video"
    PHONE = "phone"


class Appointment(Document):
    """Appointment document model."""

    patient_id: str
    doctor_id: str
    appointment_date: datetime
    duration_minutes: int = 30
    type: AppointmentType = AppointmentType.IN_PERSON
    status: AppointmentStatus = AppointmentStatus.PENDING
    reason: Optional[str] = None
    notes: Optional[str] = None
    meeting_link: Optional[str] = None
    cancellation_reason: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "appointments"
        indexes = [
            "patient_id",
            "doctor_id",
            "appointment_date",
            "status",
        ]


class AppointmentCreate(BaseModel):
    doctor_id: str
    appointment_date: datetime
    duration_minutes: int = 30
    type: AppointmentType = AppointmentType.IN_PERSON
    reason: Optional[str] = None
    notes: Optional[str] = None


class AppointmentUpdate(BaseModel):
    status: Optional[AppointmentStatus] = None
    notes: Optional[str] = None
    meeting_link: Optional[str] = None
    cancellation_reason: Optional[str] = None


class AppointmentResponse(BaseModel):
    id: str
    patient_id: str
    doctor_id: str
    appointment_date: datetime
    duration_minutes: int
    type: str
    status: str
    reason: Optional[str]
    notes: Optional[str]
    meeting_link: Optional[str]
    created_at: datetime
