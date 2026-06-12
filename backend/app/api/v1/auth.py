"""
Authentication API Routes
Login, Signup, Token Refresh, OTP, Password Reset.
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from bson import ObjectId
from app.core.security import (
    verify_password, get_password_hash, create_access_token,
    create_refresh_token, get_current_user, ROLE_PATIENT, ROLE_DOCTOR
)
from app.core.database import get_database
from app.models.user import User, UserCreate, UserLogin, UserResponse, TokenResponse, PasswordResetRequest, PasswordReset, OTPVerify
import secrets
import logging

logger = logging.getLogger("medivision.auth")
router = APIRouter()


def generate_otp() -> str:
    return str(secrets.randbelow(900000) + 100000)


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, background_tasks: BackgroundTasks):
    """Register a new user (patient or doctor)."""
    db = get_database()

    # Check if user exists
    existing = await db.users.find_one({"email": user_data.email})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Create user
    user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        role=user_data.role,
        phone=user_data.phone,
    )
    await user.create()

    # Create role-specific profile
    if user_data.role.value == ROLE_PATIENT:
        from app.models.patient import PatientProfile
        profile = PatientProfile(user_id=str(user.id))
        await profile.create()
    elif user_data.role.value == ROLE_DOCTOR:
        from app.models.doctor import DoctorProfile
        profile = DoctorProfile(user_id=str(user.id))
        await profile.create()

    # Generate OTP for email verification
    otp = generate_otp()
    await db.users.update_one(
        {"_id": user.id},
        {"$set": {"otp_code": otp}}
    )

    # Send verification email (async)
    # background_tasks.add_task(send_verification_email, user_data.email, otp)

    access_token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            role=user.role.value,
            status=user.status.value,
            phone=user.phone,
            avatar_url=user.avatar_url,
            email_verified=user.email_verified,
            created_at=user.created_at,
        ),
    )


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login with email and password."""
    db = get_database()
    user_doc = await db.users.find_one({"email": form_data.username})

    if not user_doc or not verify_password(form_data.password, user_doc["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = User(**user_doc)

    if user.status.value == "suspended":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account suspended. Contact support.",
        )

    # Update last login
    await db.users.update_one(
        {"_id": user.id},
        {"$set": {"last_login": datetime.utcnow()}}
    )

    access_token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            role=user.role.value,
            status=user.status.value,
            phone=user.phone,
            avatar_url=user.avatar_url,
            email_verified=user.email_verified,
            last_login=datetime.utcnow(),
            created_at=user.created_at,
        ),
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    """Refresh access token using refresh token."""
    from jose import jwt, JWTError
    from app.core.config import settings

    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    db = get_database()
    user_doc = await db.users.find_one({"_id": user_id})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")

    user = User(**user_doc)
    new_access_token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        user=UserResponse(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            role=user.role.value,
            status=user.status.value,
            created_at=user.created_at,
        ),
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user profile."""
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role.value,
        status=current_user.status.value,
        phone=current_user.phone,
        avatar_url=current_user.avatar_url,
        email_verified=current_user.email_verified,
        last_login=current_user.last_login,
        created_at=current_user.created_at,
    )


@router.post("/verify-otp")
async def verify_otp(data: OTPVerify):
    """Verify email with OTP code."""
    db = get_database()
    user_doc = await db.users.find_one({"email": data.email})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")

    if user_doc.get("otp_code") != data.otp_code:
        raise HTTPException(status_code=400, detail="Invalid OTP code")

    await db.users.update_one(
        {"email": data.email},
        {"$set": {"email_verified": True, "status": "active", "otp_code": None}}
    )

    return {"message": "Email verified successfully"}


@router.post("/forgot-password")
async def forgot_password(data: PasswordResetRequest):
    """Request password reset email."""
    db = get_database()
    user_doc = await db.users.find_one({"email": data.email})
    if not user_doc:
        return {"message": "If the email exists, a reset link has been sent"}

    reset_token = create_password_reset_token(data.email)
    # TODO: Send reset email with token
    logger.info(f"Password reset requested for {data.email}")

    return {"message": "If the email exists, a reset link has been sent"}


@router.post("/reset-password")
async def reset_password(data: PasswordReset):
    """Reset password using reset token."""
    from jose import jwt, JWTError
    from app.core.config import settings

    try:
        payload = jwt.decode(data.token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "password_reset":
            raise HTTPException(status_code=400, detail="Invalid token")
        email = payload.get("email")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    db = get_database()
    await db.users.update_one(
        {"email": email},
        {"$set": {"hashed_password": get_password_hash(data.new_password)}}
    )

    return {"message": "Password reset successfully"}
