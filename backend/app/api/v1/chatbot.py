"""
AI Medical Chatbot API Routes
Chat with AI assistant for medical explanations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from app.core.security import get_current_user
from app.core.database import get_database
from app.models.user import User
from app.models.chat import ChatSession, ChatMessage, ChatMessageCreate, ChatMessageResponse, ChatSessionResponse, MessageRole
from app.ai.chatbot import generate_chat_response
import logging

logger = logging.getLogger("medivision.chatbot")
router = APIRouter()


@router.post("/sessions", response_model=ChatSessionResponse)
async def create_session(
    language: str = "english",
    current_user: User = Depends(get_current_user),
):
    """Create a new chat session."""
    session = ChatSession(
        user_id=str(current_user.id),
        title="New Consultation",
        language=language,
    )
    await session.create()

    # Add system greeting
    greeting = ChatMessage(
        session_id=str(session.id),
        user_id=str(current_user.id),
        role=MessageRole.SYSTEM,
        content="Hello! I'm your AI medical assistant. I can help explain medical reports, discuss heart health, and answer health-related questions. How can I help you today?",
    )
    await greeting.create()

    return ChatSessionResponse(
        id=str(session.id),
        title=session.title,
        language=session.language,
        is_active=session.is_active,
        message_count=1,
        last_message_at=greeting.created_at,
        created_at=session.created_at,
    )


@router.get("/sessions", response_model=list[ChatSessionResponse])
async def get_sessions(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
):
    """Get user's chat sessions."""
    db = get_database()
    cursor = db.chat_sessions.find(
        {"user_id": str(current_user.id)}
    ).sort("updated_at", -1).skip(skip).limit(limit)

    sessions = []
    async for doc in cursor:
        sessions.append(ChatSessionResponse(
            id=str(doc["_id"]),
            title=doc.get("title"),
            language=doc.get("language", "english"),
            is_active=doc.get("is_active", True),
            message_count=doc.get("message_count", 0),
            last_message_at=doc.get("last_message_at"),
            created_at=doc.get("created_at", datetime.utcnow()),
        ))
    return sessions


@router.get("/sessions/{session_id}/messages", response_model=list[ChatMessageResponse])
async def get_messages(
    session_id: str,
    current_user: User = Depends(get_current_user),
):
    """Get messages in a chat session."""
    db = get_database()
    cursor = db.chat_messages.find(
        {"session_id": session_id, "user_id": str(current_user.id)}
    ).sort("created_at", 1)

    messages = []
    async for doc in cursor:
        messages.append(ChatMessageResponse(
            id=str(doc["_id"]),
            session_id=doc["session_id"],
            role=doc["role"],
            content=doc["content"],
            created_at=doc["created_at"],
        ))
    return messages


@router.post("/chat", response_model=ChatMessageResponse)
async def chat(
    message: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
):
    """Send a message to the AI chatbot and get a response."""
    db = get_database()

    # Get or create session
    session_id = message.session_id
    if not session_id:
        session = ChatSession(
            user_id=str(current_user.id),
            title=message.content[:50] + "...",
            language=message.language,
        )
        await session.create()
        session_id = str(session.id)
    else:
        session = await db.chat_sessions.find_one({"_id": session_id})
        if not session or session["user_id"] != str(current_user.id):
            raise HTTPException(status_code=404, detail="Session not found")

    # Save user message
    user_msg = ChatMessage(
        session_id=session_id,
        user_id=str(current_user.id),
        role=MessageRole.USER,
        content=message.content,
    )
    await user_msg.create()

    # Get conversation history for context
    history_cursor = db.chat_messages.find(
        {"session_id": session_id}
    ).sort("created_at", -1).limit(10)
    history = []
    async for h in history_cursor:
        history.append({"role": h["role"], "content": h["content"]})
    history.reverse()

    # Generate AI response
    try:
        ai_response = await generate_chat_response(
            user_message=message.content,
            conversation_history=history,
            language=message.language,
        )
    except Exception as e:
        logger.error(f"Chatbot error: {e}")
        ai_response = "I apologize, but I'm having trouble processing your request right now. Please try again in a moment."

    # Save AI response
    ai_msg = ChatMessage(
        session_id=session_id,
        user_id=str(current_user.id),
        role=MessageRole.ASSISTANT,
        content=ai_response,
        model_used="biogpt",
    )
    await ai_msg.create()

    # Update session
    await db.chat_sessions.update_one(
        {"_id": session_id},
        {
            "$inc": {"message_count": 2},
            "$set": {"last_message_at": datetime.utcnow(), "updated_at": datetime.utcnow()},
        },
    )

    return ChatMessageResponse(
        id=str(ai_msg.id),
        session_id=session_id,
        role=ai_msg.role.value,
        content=ai_msg.content,
        created_at=ai_msg.created_at,
    )


@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
):
    """Delete a chat session and all its messages."""
    db = get_database()
    session = await db.chat_sessions.find_one({"_id": session_id})

    if not session or session["user_id"] != str(current_user.id):
        raise HTTPException(status_code=404, detail="Session not found")

    await db.chat_messages.delete_many({"session_id": session_id})
    await db.chat_sessions.delete_one({"_id": session_id})

    return {"message": "Session deleted successfully"}
