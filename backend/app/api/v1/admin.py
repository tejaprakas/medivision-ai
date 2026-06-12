"""
Admin API Routes
User management, platform administration.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.security import get_current_user, require_admin
from app.core.database import get_database
from app.models.user import User, UserResponse, UserStatus
import logging

logger = logging.getLogger("medivision.admin")
router = APIRouter()


@router.get("/users", response_model=list[UserResponse])
async def list_users(
    role: str = Query(None),
    status: str = Query(None),
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(require_admin),
):
    """List all users with filtering."""
    db = get_database()
    query = {}
    if role:
        query["role"] = role
    if status:
        query["status"] = status

    cursor = db.users.find(query).sort("created_at", -1).skip(skip).limit(limit)
    users = []
    async for doc in cursor:
        users.append(UserResponse(
            id=str(doc["_id"]),
            email=doc["email"],
            full_name=doc.get("full_name", ""),
            role=doc.get("role", ""),
            status=doc.get("status", ""),
            phone=doc.get("phone"),
            avatar_url=doc.get("avatar_url"),
            email_verified=doc.get("email_verified", False),
            created_at=doc.get("created_at"),
        ))
    return users


@router.patch("/users/{user_id}/status")
async def update_user_status(
    user_id: str,
    new_status: str,
    current_user: User = Depends(require_admin),
):
    """Update user status (active, inactive, suspended)."""
    db = get_database()
    try:
        status = UserStatus(new_status)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status")

    result = await db.users.update_one(
        {"_id": user_id},
        {"$set": {"status": status.value}},
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": f"User status updated to {status.value}"}


@router.get("/stats")
async def get_platform_stats(current_user: User = Depends(require_admin)):
    """Get platform-wide statistics."""
    db = get_database()

    return {
        "total_users": await db.users.count_documents({}),
        "total_patients": await db.users.count_documents({"role": "patient"}),
        "total_doctors": await db.users.count_documents({"role": "doctor"}),
        "total_analyses": await db.analysis_results.count_documents({}),
        "total_reports": await db.medical_reports.count_documents({}),
        "total_appointments": await db.appointments.count_documents({}),
    }
