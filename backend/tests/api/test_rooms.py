import pytest
from app.main import app
from app.models.player import Player
from app.models.problem import OpBounds, Operation
from app.models.room import Room
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def room(client: TestClient) -> dict:
    return client.post("/rooms/", params={"host": "Host"}).json()


def test_create_room(client: TestClient) -> None:
    res = client.post("/rooms/", params={"host": "Host"})

    assert res.status_code == 201
    assert res.json() is not None


def test_get_room(client: TestClient, room: dict) -> None:
    res = client.get(f"/rooms/{room['id']}")

    assert res.status_code == 200
    assert res.json() == room


def test_get_nonexistent_room(client: TestClient) -> None:
    res = client.get("/rooms/nonexistent")

    assert res.status_code == 404
    assert res.json() is None


def test_get_rooms(client: TestClient) -> None:
    res = client.get("/rooms/")

    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_delete_room(client: TestClient, room: dict) -> None:
    res = client.delete(f"/rooms/{room['id']}")

    assert res.status_code == 204


def test_delete_nonexistent_room(client: TestClient) -> None:
    res = client.delete("/rooms/nonexistent")

    assert res.status_code == 404


def test_add_player(client: TestClient, room: dict) -> None:
    res = client.post(f"/rooms/add/{room['id']}", params={"player": "Alice"})

    assert res.status_code == 200
    assert res.json() is not None


def test_add_player_nonexistent_room(client: TestClient) -> None:
    res = client.post("/rooms/add/nonexistent", params={"player": "Alice"})

    assert res.status_code == 404
    assert res.json() is None


def test_add_player_already_in(client: TestClient, room: dict) -> None:
    res = client.post(f"/rooms/add/{room['id']}", params={"player": "Alice"})
    assert res.status_code == 200
    assert res.json() is not None

    res = client.post(f"/rooms/add/{room['id']}", params={"player": "Alice"})
    assert res.status_code == 404
    assert res.json() is None


def test_remove_player(client: TestClient, room: dict) -> None:
    res = client.post(f"/rooms/add/{room['id']}", params={"player": "Alice"})
    assert res.status_code == 200
    assert res.json() is not None

    res = client.post(f"/rooms/remove/{room['id']}", params={"player": "Alice"})
    assert res.status_code == 200
    assert res.json() is None


# def test_leave_room_last_player(manager: Manager, room: Room, host: Player) -> None:
#     assert manager.leave_room(room.id, host) is True
#     assert host.name not in room.players
#     assert room.id not in manager.rooms


# def test_leave_nonexistent_room(manager: Manager, player_1: Player) -> None:
#     assert manager.leave_room("nonexistent", player_1) is False


# def test_leave_room_player_not_in(
#     manager: Manager, room: Room, player_1: Player
# ) -> None:
#     assert manager.leave_room(room.id, player_1) is False


# def test_start_match(manager: Manager, room: Room) -> None:
#     assert manager.start_match(room.id) is True


# def test_start_match_nonexistent_room(manager: Manager) -> None:
#     assert manager.start_match("nonexistent") is False


# def test_start_match_already_started(manager: Manager, room: Room) -> None:
#     manager.start_match(room.id)
#     assert manager.start_match(room.id) is False


# def test_end_match(manager: Manager, room: Room) -> None:
#     manager.start_match(room.id)
#     assert manager.end_match(room.id) is True


# def test_end_match_nonexistent_room(manager: Manager) -> None:
#     assert manager.end_match("nonexistent") is False


# def test_end_match_already_ended(manager: Manager, room: Room) -> None:
#     manager.start_match(room.id)
#     manager.end_match(room.id)
#     assert manager.end_match(room.id) is False


# def test_handle_answer_correct(manager: Manager, room: Room, host: Player) -> None:
#     manager.start_match(room.id)
#     assert manager.handle_answer(room.id, host, 3) is True


# def test_handle_answer_incorrect(manager: Manager, room: Room, host: Player) -> None:
#     manager.start_match(room.id)
#     assert manager.handle_answer(room.id, host, 0) is False


# def test_handle_answer_nonexistent_room(manager: Manager, host: Player) -> None:
#     assert manager.handle_answer("nonexistent", host, 0) is False


# def test_handle_answer_nonexistent_match(
#     manager: Manager, room: Room, host: Player
# ) -> None:
#     assert manager.handle_answer(room.id, host, 0) is False


# def test_handle_answer_nonexistent_player(
#     manager: Manager, room: Room, player_1: Player
# ) -> None:
#     manager.start_match(room.id)
#     assert manager.handle_answer(room.id, player_1, 0) is False
