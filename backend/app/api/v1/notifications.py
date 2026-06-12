"""
Notification API Routes
Manage user notifications and real-time alerts.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.security import get_current_user
from app.core.database import get_database
from app.models.user import User
from app.models.notification import NotificationResponse
import logging

logger = logging.getLogger("medivision.notifications")
router = APIRouter()


@router.get("/", response_model=list[NotificationResponse])
async def get_notifications(
    unread_only: bool = Query(False),
    limit: int = 50,
    current_user: User = Depends(get_current_user),
):
    """Get user notifications."""
    db = get_database()
    query = {"user_id": str(current_user.id)}
    if unread_only:
        query["is_read"] = False

    cursor = db.notifications.find(query).sort("created_at", -1).limit(limit)
    notifications = []
    async for doc in cursor:
        notifications.append(NotificationResponse(
            id=str(doc["_id"]),
            type=doc.get("type", ""),
            priority=doc.get("priority", "normal"),
            title=doc.get("title", ""),
            message=doc.get("message", ""),
            is_read=doc.get("is_read", False),
            action_url=doc.get("action_url"),
            created_at=doc.get("created_at"),
        ))
    return notifications


@router.post("/{notification_id}/read")
async def mark_as_read(
    notification_id: str,
    current_user: User = Depends(get_current_user),
):
    """Mark notification as read."""
    db = get_database()
    result = await db.notifications.update_one(
        {"_id": notification_id, "user_id": str(current_user.id)},
        {"$set": {"is_read": True, "read_at": datetime.utcnow()}},
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Marked as read"}


@router.post("/read-all")
async def mark_all_as_read(current_user: User = Depends(get_current_user)):
    """Mark all notifications as read."""
    db = get_database()
    await db.notifications.update_many(
        {"user_id": str(current_user.id), "is_read": False},
        {"$set": {"is_read": True, "read_at": datetime.utcnow()}},
    )
    return {"message": "All notifications marked as read"}


@router.get("/unread-count")
async def get_unread_count(current_user: User = Depends(get_current_user)):
    """Get count of unread notifications."""
    db = get_database()
    count = await db.notifications.count_documents({
        "user_id": str(current_user.id),
        "is_read": False,
    })
    return {"unread_count": count}
