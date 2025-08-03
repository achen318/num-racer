from fastapi import APIRouter

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"],
)

rooms = []


@router.get("/")
def read_rooms():
    return rooms


@router.post("/")
def create_room():
    room = {"id": len(rooms) + 1, "players": [], "match": None}
    rooms.append(room)
    return room


@router.get("/{room_id}")
def read_room(room_id: int):
    for room in rooms:
        if room["id"] == room_id:
            return room

    return None


@router.post("/{room_id}/join")
def join_room(room_id: int, player: str):
    room = read_room(room_id)

    if room and player not in room["players"]:
        room["players"].append(player)
        return True

    return False


@router.post("/{room_id}/leave")
def leave_room(room_id: int, player: str):
    room = read_room(room_id)

    if room and player in room["players"]:
        room["players"].remove(player)
        return True

    return False


@router.post("/{room_id}/start")
def start_game(room_id: int):
    room = read_room(room_id)

    if room:
        room["match"] = {"status": "in_progress"}
        return True

    return False
