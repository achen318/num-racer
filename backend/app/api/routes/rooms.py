from app.models.manager import Manager
from app.models.match import MatchSettings
from app.models.player import Player
from app.models.room import Room
from fastapi import APIRouter, Response, status

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"],
)

manager = Manager()


@router.get("/{room_id}")
def get_room(room_id: str, response: Response) -> Room | None:
    if room := manager.get_room(room_id):
        return room

    response.status_code = status.HTTP_404_NOT_FOUND
    return None


@router.get("/")
def get_rooms() -> list[Room]:
    return manager.get_rooms()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_room(host: str) -> Room:
    return manager.create_room(Player(name=host))


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: str, response: Response) -> None:
    if manager.delete_room(room_id):
        return

    response.status_code = status.HTTP_404_NOT_FOUND


@router.post("/add/{room_id}")
def add_player(room_id: str, player: str, response: Response) -> Room | None:
    if room := manager.add_player(room_id, Player(name=player)):
        return room

    response.status_code = status.HTTP_404_NOT_FOUND
    return None


@router.post("/remove/{room_id}")
def remove_player(room_id: str, player: str, response: Response) -> None:
    if manager.remove_player(room_id, Player(name=player)):
        return

    response.status_code = status.HTTP_404_NOT_FOUND


@router.post("/update_settings/{room_id}")
def update_settings(room_id: str, settings: dict, response: Response) -> None:
    if manager.update_settings(room_id, settings):
        return

    response.status_code = status.HTTP_404_NOT_FOUND


@router.post("/start/{room_id}", status_code=status.HTTP_201_CREATED)
def start_match(room_id: str, response: Response) -> None:
    if manager.start_match(room_id):
        return

    response.status_code = status.HTTP_404_NOT_FOUND


@router.post("/end/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def end_match(room_id: str, response: Response) -> None:
    if manager.end_match(room_id):
        return

    response.status_code = status.HTTP_404_NOT_FOUND
