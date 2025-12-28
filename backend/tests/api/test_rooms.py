import pytest
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def room(client: TestClient) -> dict:
    my_room = client.post("/rooms/", params={"host": "Host"}).json()

    client.post(
        f"/rooms/update_settings/{my_room['id']}",
        json={
            "operations": ["+"],
            "add_bounds": {"bounds_1": [1, 1], "bounds_2": [2, 2]},
        },
    )

    return client.get(f"/rooms/{my_room['id']}").json()


@pytest.fixture
def host() -> dict:
    return {"player": "Host"}


@pytest.fixture
def player_1() -> dict:
    return {"player": "Alice"}


@pytest.fixture
def player_2() -> dict:
    return {"player": "Bob"}


@pytest.fixture
def settings() -> dict:
    return {
        "operations": ["-"],
        "add_bounds": {"bounds_1": [3, 3], "bounds_2": [4, 4]},
    }


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


def test_add_player(client: TestClient, room: dict, player_1: dict) -> None:
    res = client.post(f"/rooms/add/{room['id']}", params=player_1)

    assert res.status_code == 200
    assert res.json() is not None


def test_add_player_nonexistent_room(client: TestClient, player_1: dict) -> None:
    res = client.post("/rooms/add/nonexistent", params=player_1)

    assert res.status_code == 404


def test_add_player_already_in(client: TestClient, room: dict, player_1: dict) -> None:
    res = client.post(f"/rooms/add/{room['id']}", params=player_1)
    assert res.status_code == 200
    assert res.json() is not None

    res = client.post(f"/rooms/add/{room['id']}", params=player_1)
    assert res.status_code == 404


def test_remove_player(client: TestClient, room: dict, player_1: dict) -> None:
    res = client.post(f"/rooms/add/{room['id']}", params=player_1)
    assert res.status_code == 200
    assert res.json() is not None

    res = client.post(f"/rooms/remove/{room['id']}", params=player_1)
    assert res.status_code == 204


def test_remove_player_last_player(client: TestClient, room: dict, host: dict) -> None:
    res = client.post(f"/rooms/remove/{room['id']}", params=host)
    assert res.status_code == 204

    res = client.get(f"/rooms/{room['id']}")
    assert res.status_code == 404


def test_remove_player_nonexistent_room(client: TestClient, player_1: dict) -> None:
    res = client.post("/rooms/remove/nonexistent", params=player_1)

    assert res.status_code == 404


def test_update_settings(client: TestClient, room: dict, settings: dict) -> None:
    res = client.post(f"/rooms/update_settings/{room['id']}", json=settings)

    assert res.status_code == 204


def test_update_settings_nonexistent_room(client: TestClient, settings: dict) -> None:
    res = client.post("/rooms/update_settings/nonexistent", json=settings)

    assert res.status_code == 404


def test_start_match(client: TestClient, room: dict) -> None:
    res = client.post(f"/rooms/start/{room['id']}")

    assert res.status_code == 201
    assert res.json() is None


def test_start_match_nonexistent_room(client: TestClient) -> None:
    res = client.post("/rooms/start/nonexistent")

    assert res.status_code == 404


def test_start_match_already_started(client: TestClient, room: dict) -> None:
    client.post(f"/rooms/start/{room['id']}")
    res = client.post(f"/rooms/start/{room['id']}")

    assert res.status_code == 404


def test_end_match(client: TestClient, room: dict) -> None:
    client.post(f"/rooms/start/{room['id']}")
    res = client.post(f"/rooms/end/{room['id']}")

    assert res.status_code == 204


def test_end_match_nonexistent_room(client: TestClient) -> None:
    res = client.post("/rooms/end/nonexistent")

    assert res.status_code == 404


def test_end_match_already_ended(client: TestClient, room: dict) -> None:
    res = client.post(f"/rooms/end/{room['id']}")

    assert res.status_code == 404


def test_handle_answer_correct(client: TestClient, room: dict, host: dict) -> None:
    client.post(f"/rooms/start/{room['id']}")
    res = client.post(
        f"/rooms/answer/{room['id']}",
        params=host | {"answer": 3},
    )

    assert res.status_code == 200
    assert res.json() is True


def test_handle_answer_incorrect(client: TestClient, room: dict, host: dict) -> None:
    client.post(f"/rooms/start/{room['id']}")
    res = client.post(
        f"/rooms/answer/{room['id']}",
        params=host | {"answer": 0},
    )

    assert res.status_code == 200
    assert res.json() is False


def test_handle_answer_nonexistent_room(client: TestClient, host: dict) -> None:
    res = client.post(
        "/rooms/answer/nonexistent",
        params=host | {"answer": 0},
    )

    assert res.status_code == 404


def test_handle_answer_nonexistent_match(
    client: TestClient, room: dict, host: dict
) -> None:
    res = client.post(
        f"/rooms/answer/{room['id']}",
        params=host | {"answer": 0},
    )

    assert res.status_code == 404


def test_handle_answer_nonexistent_player(client: TestClient, room: dict) -> None:
    client.post(f"/rooms/start/{room['id']}")
    res = client.post(
        f"/rooms/answer/{room['id']}",
        params={"player": "Nonexistent", "answer": 0},
    )

    assert res.status_code == 404
