"""
Notification Service
Create and manage user notifications.
"""

from datetime import datetime
from app.models.notification import Notification, NotificationType, NotificationPriority
from app.core.database import get_database
from app.api.websocket.notifications import send_notification
import logging

logger = logging.getLogger("medivision.notifications")


async def create_notification(
    user_id: str,
    type: NotificationType,
    title: str,
    message: str,
    priority: NotificationPriority = NotificationPriority.NORMAL,
    data: dict = None,
    action_url: str = None,
):
    """Create a notification and send it via WebSocket."""
    notification = Notification(
        user_id=user_id,
        type=type,
        priority=priority,
        title=title,
        message=message,
        data=data,
        action_url=action_url,
    )
    await notification.create()

    # Send real-time notification via WebSocket
    await send_notification(user_id, {
        "type": "notification",
        "notification_type": type.value,
        "priority": priority.value,
        "title": title,
        "message": message,
        "data": data,
        "action_url": action_url,
        "created_at": datetime.utcnow().isoformat(),
    })

    return notification


async def get_user_notifications(user_id: str, unread_only: bool = False, limit: int = 50):
    """Get notifications for a user."""
    db = get_database()
    query = {"user_id": user_id}
    if unread_only:
        query["is_read"] = False

    cursor = db.notifications.find(query).sort("created_at", -1).limit(limit)
    notifications = []
    async for doc in cursor:
        notifications.append({
            "id": str(doc["_id"]),
            "type": doc.get("type", ""),
            "priority": doc.get("priority", "normal"),
            "title": doc.get("title", ""),
            "message": doc.get("message", ""),
            "is_read": doc.get("is_read", False),
            "action_url": doc.get("action_url"),
            "created_at": doc.get("created_at"),
        })
    return notifications
