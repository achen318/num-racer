"""
Represents a manager that handles websocket connections and messaging per room.
"""

from fastapi import WebSocket
from pydantic import BaseModel

from .schemas import WebSocketMessage


class WebSocketManager(BaseModel):
    """
    Represents a manager that handles websocket connections and messaging per
    room.
    """

    rooms: dict[str, list[WebSocket]] = {}

    async def connect(self, room_id: str, websocket: WebSocket) -> None:
        """
        Connects a websocket to a room.

        Args:
            room_id: The ID of the room to connect to.
            websocket: The websocket to connect.
        """
        await websocket.accept()
        self.rooms[room_id].append(websocket)

    def disconnect(self, room_id: str, websocket: WebSocket) -> None:
        """
        Disconnects a websocket from a room.

        Args:
            room_id: The ID of the room to disconnect from.
            websocket: The websocket to disconnect.
        """
        self.rooms[room_id].remove(websocket)
        if not self.rooms[room_id]:
            del self.rooms[room_id]

    async def send(self, websocket: WebSocket, message: WebSocketMessage) -> None:
        await websocket.send_json(message.payload)

    async def broadcast(self, room_id: str, message: WebSocketMessage) -> None:
        for connection in self.rooms.get(room_id, []):
            await connection.send_json(message.payload)
