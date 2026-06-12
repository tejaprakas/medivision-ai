"""
WebSocket Handler for Real-Time Notifications
"""

import json
import logging
from typing import Dict, Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.core.security import get_current_user
from app.models.user import User

logger = logging.getLogger("medivision.websocket")
router = APIRouter()

# Active WebSocket connections: user_id -> set of WebSocket connections
active_connections: Dict[str, Set[WebSocket]] = {}


async def connect(websocket: WebSocket, user_id: str):
    """Register a new WebSocket connection."""
    await websocket.accept()
    if user_id not in active_connections:
        active_connections[user_id] = set()
    active_connections[user_id].add(websocket)
    logger.info(f"WebSocket connected for user {user_id}")


def disconnect(websocket: WebSocket, user_id: str):
    """Remove a WebSocket connection."""
    if user_id in active_connections:
        active_connections[user_id].discard(websocket)
        if not active_connections[user_id]:
            del active_connections[user_id]
    logger.info(f"WebSocket disconnected for user {user_id}")


async def send_notification(user_id: str, notification: dict):
    """Send a notification to a specific user."""
    if user_id in active_connections:
        disconnected = set()
        for ws in active_connections[user_id]:
            try:
                await ws.send_json(notification)
            except Exception:
                disconnected.add(ws)

        # Clean up disconnected sockets
        for ws in disconnected:
            disconnect(ws, user_id)


async def broadcast(notification: dict):
    """Broadcast a notification to all connected users."""
    for user_id in list(active_connections.keys()):
        await send_notification(user_id, notification)


@router.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket):
    """WebSocket endpoint for real-time notifications."""
    # Authenticate via query parameter token
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=4001, reason="Missing authentication token")
        return

    try:
        from jose import jwt, JWTError
        from app.core.config import settings
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            await websocket.close(code=4001, reason="Invalid token")
            return
    except JWTError:
        await websocket.close(code=4001, reason="Invalid token")
        return

    await connect(websocket, user_id)

    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            message = json.loads(data)

            # Handle ping/pong
            if message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        disconnect(websocket, user_id)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        disconnect(websocket, user_id)
