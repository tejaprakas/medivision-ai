"""
User Model
Core user document with authentication fields.
"""

from beanie import Document, Indexed
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"


class User(Document):
    """User document model for MongoDB."""

    email: Indexed(str, unique=True)
    hashed_password: str
    full_name: str
    role: UserRole = UserRole.PATIENT
    status: UserStatus = UserStatus.PENDING_VERIFICATION
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    email_verified: bool = False
    otp_code: Optional[str] = None
    otp_expires: Optional[datetime] = None
    refresh_token: Optional[str] = None
    last_login: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
        indexes = [
            "email",
            "role",
            "status",
            "created_at",
        ]

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "full_name": "John Doe",
                "role": "patient",
                "status": "active",
            }
        }


# Pydantic Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=2)
    role: UserRole = UserRole.PATIENT
    phone: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    status: str
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    email_verified: bool
    last_login: Optional[datetime] = None
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordReset(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)


class OTPVerify(BaseModel):
    email: EmailStr
    otp_code: str
