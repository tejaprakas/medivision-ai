"""
Patient Profile Model
Extended profile information for patient users.
"""

from beanie import Document, Link
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class BloodGroup(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class Allergy(BaseModel):
    allergen: str
    severity: str = "moderate"  # mild, moderate, severe
    notes: Optional[str] = None


class Medication(BaseModel):
    name: str
    dosage: str
    frequency: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class MedicalCondition(BaseModel):
    condition: str
    diagnosed_date: Optional[datetime] = None
    status: str = "active"  # active, resolved, managed
    notes: Optional[str] = None


class EmergencyContact(BaseModel):
    name: str
    relationship: str
    phone: str


class PatientProfile(Document):
    """Patient profile document model."""

    user_id: str
    age: Optional[int] = None
    gender: Optional[Gender] = None
    blood_group: Optional[BloodGroup] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = "India"
    pincode: Optional[str] = None
    emergency_contact: Optional[EmergencyContact] = None
    allergies: List[Allergy] = []
    current_medications: List[Medication] = []
    medical_conditions: List[MedicalCondition] = []
    medical_history_notes: Optional[str] = None
    health_score: Optional[float] = None  # 0-100
    total_analyses: int = 0
    total_reports: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "patient_profiles"
        indexes = [
            "user_id",
            "blood_group",
            "age",
        ]


class PatientProfileCreate(BaseModel):
    age: Optional[int] = None
    gender: Optional[Gender] = None
    blood_group: Optional[BloodGroup] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: str = "India"
    pincode: Optional[str] = None
    emergency_contact: Optional[EmergencyContact] = None
    allergies: List[Allergy] = []
    current_medications: List[Medication] = []
    medical_conditions: List[MedicalCondition] = []
    medical_history_notes: Optional[str] = None


class PatientProfileUpdate(BaseModel):
    age: Optional[int] = None
    gender: Optional[Gender] = None
    blood_group: Optional[BloodGroup] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    emergency_contact: Optional[EmergencyContact] = None
    allergies: Optional[List[Allergy]] = None
    current_medications: Optional[List[Medication]] = None
    medical_conditions: Optional[List[MedicalCondition]] = None
    medical_history_notes: Optional[str] = None


class PatientProfileResponse(BaseModel):
    id: str
    user_id: str
    age: Optional[int]
    gender: Optional[str]
    blood_group: Optional[str]
    height_cm: Optional[float]
    weight_kg: Optional[float]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: str
    health_score: Optional[float]
    total_analyses: int
    total_reports: int
    created_at: datetime
