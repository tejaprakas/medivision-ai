"""
Doctor Profile Model
Extended profile information for doctor users.
"""

from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class DoctorProfile(Document):
    """Doctor profile document model."""

    user_id: str
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    license_number: Optional[str] = None
    hospital: Optional[str] = None
    experience_years: Optional[int] = None
    consultation_fee: Optional[float] = None
    about: Optional[str] = None
    available_days: List[str] = []  # ["Monday", "Tuesday", ...]
    available_time_start: Optional[str] = None  # "09:00"
    available_time_end: Optional[str] = None  # "17:00"
    rating: float = 0.0
    total_reviews: int = 0
    total_patients: int = 0
    is_available: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "doctor_profiles"
        indexes = [
            "user_id",
            "specialization",
            "license_number",
            "is_available",
        ]


class DoctorProfileCreate(BaseModel):
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    license_number: Optional[str] = None
    hospital: Optional[str] = None
    experience_years: Optional[int] = None
    consultation_fee: Optional[float] = None
    about: Optional[str] = None
    available_days: List[str] = []
    available_time_start: Optional[str] = None
    available_time_end: Optional[str] = None


class DoctorProfileUpdate(BaseModel):
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    license_number: Optional[str] = None
    hospital: Optional[str] = None
    experience_years: Optional[int] = None
    consultation_fee: Optional[float] = None
    about: Optional[str] = None
    available_days: Optional[List[str]] = None
    available_time_start: Optional[str] = None
    available_time_end: Optional[str] = None
    is_available: Optional[bool] = None


class DoctorProfileResponse(BaseModel):
    id: str
    user_id: str
    full_name: str = ""
    email: str = ""
    qualification: Optional[str]
    specialization: Optional[str]
    license_number: Optional[str]
    hospital: Optional[str]
    experience_years: Optional[int]
    consultation_fee: Optional[float]
    about: Optional[str]
    available_days: List[str]
    rating: float
    total_reviews: int
    total_patients: int
    is_available: bool
