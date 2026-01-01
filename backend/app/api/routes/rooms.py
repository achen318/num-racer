"""
Contains all room-related API routes.
"""

from app.models.manager import Manager
from app.models.match import MatchSettings
from app.models.player import Player
from app.models.room import Room
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/rooms", tags=["room"])
manager = Manager()


ROOM_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Room not found",
)


@router.get(
    "/{room_id}",
    response_model=Room,
    responses={404: {"description": "Room not found"}},
)
def get_room(room_id: str) -> Room:
    """
    Returns the room with the given ID.
    """
    if room := manager.get_room(room_id):
        return room

    raise ROOM_NOT_FOUND


@router.get("/", response_model=list[Room])
def get_rooms() -> list[Room]:
    """
    Returns a list of all active rooms.
    """
    return manager.get_rooms()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Room created successfully"},
    },
)
def create_room(host: str) -> str:
    """
    Creates a new room with the given player as the host.
    """
    return manager.create_room(Player(name=host))


@router.delete(
    "/{room_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Room deleted successfully"},
        404: {"description": "Room not found"},
    },
)
def delete_room(room_id: str) -> None:
    """
    Deletes the room with the given ID.
    """
    if manager.delete_room(room_id):
        return None

    raise ROOM_NOT_FOUND


@router.post(
    "/add/{room_id}",
    responses={404: {"description": "Room or player not found"}},
)
def add_player(room_id: str, player: str) -> bool:
    """
    Adds a player to the room with the given ID.
    """
    if manager.add_player(room_id, Player(name=player)):
        return True

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Room or player not found",
    )


@router.post(
    "/remove/{room_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Player removed successfully"},
        404: {"description": "Room not found"},
    },
)
def remove_player(room_id: str, player: str) -> None:
    """
    Removes a player from the room with the given ID. If no more players
    remain in the room, the room is deleted.
    """
    if manager.remove_player(room_id, Player(name=player)):
        return None

    raise ROOM_NOT_FOUND


@router.post(
    "/update_settings/{room_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Settings updated successfully"},
        404: {"description": "Room not found"},
    },
)
def update_settings(room_id: str, settings: dict) -> None:
    """
    Update the match settings for the room with the given ID.
    """
    if manager.update_settings(room_id, MatchSettings(**settings)):
        return None

    raise ROOM_NOT_FOUND


@router.post(
    "/start/{room_id}",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Match started successfully"},
        404: {"description": "Room not found"},
    },
)
def start_match(room_id: str) -> None:
    """
    Starts the match for the room with the given ID.
    """
    if manager.start_match(room_id):
        return None

    raise ROOM_NOT_FOUND


@router.post(
    "/end/{room_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Match ended successfully"},
        404: {"description": "Room not found"},
    },
)
def end_match(room_id: str) -> None:
    """
    Ends the match for the room with the given ID.
    """
    if manager.end_match(room_id):
        return None

    raise ROOM_NOT_FOUND


@router.post(
    "/answer/{room_id}",
    responses={
        404: {"description": "Room, match, or player not found"},
    },
)
def handle_answer(room_id: str, player: str, answer: int) -> bool:
    """
    Handles a player's answer for the room with the given ID."""
    verdict = manager.handle_answer(room_id, Player(name=player), answer)

    if verdict is not None:
        return verdict

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Room, match, or player not found",
    )
