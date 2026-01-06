"""
Represents a websocket message schema.
"""

from enum import StrEnum

from pydantic import BaseModel


class MessageType(StrEnum):
    """
    Represents the type of websocket message.
    """

    JOIN = "join"
    LEAVE = "leave"
    UPDATE = "update"


class WebSocketMessage(BaseModel):
    """
    Represents a websocket message schema.
    """

    type: MessageType
    room_id: str | None = None
    player: str | None = None
    payload: dict = {}
