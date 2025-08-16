from fastapi import APIRouter, Response, status
from pydantic import BaseModel

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"],
)

rooms = []


class Player(BaseModel):
    name: str


class Match(BaseModel):
    status: str


class Room(BaseModel):
    id: int
    players: list[Player]
    match: Match | None


@router.get("/")
def read_rooms() -> list[Room]:
    return rooms


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_room() -> Room:
    room = Room(id=len(rooms) + 1, players=[], match=None)
    rooms.append(room)
    return room


@router.get("/{room_id}")
def read_room(room_id: int, response: Response) -> Room | None:
    for room in rooms:
        if room.id == room_id:
            return room

    response.status_code = status.HTTP_404_NOT_FOUND


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: int, response: Response) -> None:
    for i, room in enumerate(rooms):
        if room.id == room_id:
            if room.players:
                response.status_code = status.HTTP_400_BAD_REQUEST
            else:
                del rooms[i]

            return

    response.status_code = status.HTTP_404_NOT_FOUND


@router.post("/join")
def join_room(room_id: int, player: str, response: Response) -> Room | None:
    room = read_room(room_id, response)

    if room and player not in {p.name for p in room.players}:
        room.players.append(Player(name=player))
        return room

    response.status_code = status.HTTP_404_NOT_FOUND


@router.post("/leave")
def leave_room(room_id: int, player: str, response: Response) -> Room | None:
    room = read_room(room_id, response)

    if room and player in {p.name for p in room.players}:
        room.players.remove(Player(name=player))
        return room

    response.status_code = status.HTTP_404_NOT_FOUND


@router.post("/start", status_code=status.HTTP_201_CREATED)
def start_game(room_id: int, response: Response) -> Room | None:
    if room := read_room(room_id, response):
        room.match = Match(status="in_progress")
        return room
