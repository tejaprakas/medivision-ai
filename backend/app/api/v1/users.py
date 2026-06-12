"""
User Profile API Routes
Manage user profiles and settings.
"""

from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.core.database import get_database
from app.models.user import User, UserResponse
import logging

logger = logging.getLogger("medivision.users")
router = APIRouter()


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
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


@router.put("/profile")
async def update_profile(
    full_name: str = None,
    phone: str = None,
    current_user: User = Depends(get_current_user),
):
    """Update user profile."""
    db = get_database()
    update_data = {}
    if full_name:
        update_data["full_name"] = full_name
    if phone:
        update_data["phone"] = phone

    if update_data:
        await db.users.update_one({"_id": current_user.id}, {"$set": update_data})

    return {"message": "Profile updated successfully"}
