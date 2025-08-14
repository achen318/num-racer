from fastapi import APIRouter, Response, status
from pydantic import BaseModel

from rooms import rooms, Room

router = APIRouter(
    prefix="/match",
    tags=["match", "room"]
)

@router.get("/{room_id}")
def get_match(room_id: int, response: Response):
    room = next((r for r in rooms if r.id == room_id), None)
    if room and room.match:
        return room.match
    response.status_code = status.HTTP_404_NOT_FOUND
