"""
Security Utilities
JWT token creation, password hashing, and role-based access control.
"""

from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, WebSocketException
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.core.database import get_database
from app.models.user import User
import logging

logger = logging.getLogger("medivision.security")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Role constants
ROLE_PATIENT = "patient"
ROLE_DOCTOR = "doctor"
ROLE_ADMIN = "admin"
ROLES = [ROLE_PATIENT, ROLE_DOCTOR, ROROLE_ADMIN]


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict) -> str:
    """Create a JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_verification_token(email: str) -> str:
    """Create email verification token."""
    expire = datetime.utcnow() + timedelta(hours=24)
    return jwt.encode(
        {"email": email, "exp": expire, "type": "verification"},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def create_password_reset_token(email: str) -> str:
    """Create password reset token."""
    expire = datetime.utcnow() + timedelta(hours=1)
    return jwt.encode(
        {"email": email, "exp": expire, "type": "password_reset"},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        if user_id is None or token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db = get_database()
    user_doc = await db.users.find_one({"_id": user_id})
    if user_doc is None:
        raise credentials_exception

    return User(**user_doc)


def require_role(*roles: str):
    """Dependency factory for role-based access control."""
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role(s): {', '.join(roles)}",
            )
        return current_user
    return role_checker


# Role-specific dependencies
require_patient = require_role(ROLE_PATIENT)
require_doctor = require_role(ROLE_DOCTOR)
require_admin = require_role(ROLE_ADMIN)
require_doctor_or_admin = require_role(ROLE_DOCTOR, ROLE_ADMIN)
require_any_authenticated = require_role(ROLE_PATIENT, ROLE_DOCTOR, ROLE_ADMIN)
