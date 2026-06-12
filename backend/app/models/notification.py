"""
Notification Model
Stores user notifications for real-time alerts.
"""

from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class NotificationType(str, Enum):
    ANALYSIS_COMPLETE = "analysis_complete"
    REPORT_READY = "report_ready"
    APPOINTMENT_REMINDER = "appointment_reminder"
    APPOINTMENT_CONFIRMED = "appointment_confirmed"
    EMERGENCY_ALERT = "emergency_alert"
    SYSTEM = "system"
    CHAT_MESSAGE = "chat_message"


class NotificationPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class Notification(Document):
    """Notification document model."""

    user_id: str
    type: NotificationType
    priority: NotificationPriority = NotificationPriority.NORMAL
    title: str
    message: str
    data: Optional[dict] = None  # Additional JSON data
    is_read: bool = False
    read_at: Optional[datetime] = None
    action_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "notifications"
        indexes = [
            "user_id",
            "is_read",
            "type",
            "created_at",
        ]


class NotificationResponse(BaseModel):
    id: str
    type: str
    priority: str
    title: str
    message: str
    is_read: bool
    action_url: Optional[str]
    created_at: datetime
