"""
Chat Message Model
Stores chatbot conversation history.
"""

from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatSession(Document):
    """Chat session document model."""

    user_id: str
    title: Optional[str] = None
    language: str = "english"
    is_active: bool = True
    message_count: int = 0
    last_message_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "chat_sessions"
        indexes = [
            "user_id",
            "is_active",
            "created_at",
        ]


class ChatMessage(Document):
    """Individual chat message document model."""

    session_id: str
    user_id: str
    role: MessageRole
    content: str
    tokens_used: Optional[int] = None
    model_used: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "chat_messages"
        indexes = [
            "session_id",
            "user_id",
            "created_at",
        ]


class ChatMessageCreate(BaseModel):
    session_id: Optional[str] = None
    content: str
    language: str = "english"


class ChatMessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    created_at: datetime


class ChatSessionResponse(BaseModel):
    id: str
    title: Optional[str]
    language: str
    is_active: bool
    message_count: int
    last_message_at: Optional[datetime]
    created_at: datetime
