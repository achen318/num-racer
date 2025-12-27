import pytest
from app.models.manager import Manager
from app.models.match import MatchSettings
from app.models.player import Player
from app.models.problem import OpBounds, Operation
from app.models.room import Room


@pytest.fixture
def manager() -> Manager:
    return Manager()


@pytest.fixture
def room(manager: Manager, host: Player) -> Room:
    rm = manager.create_room(host)

    rm.match_settings.operations = [Operation.ADD]
    rm.match_settings.add_bounds = OpBounds(bounds_1=(1, 1), bounds_2=(2, 2))

    return rm


@pytest.fixture
def host() -> Player:
    return Player(name="Host")


@pytest.fixture
def player_1() -> Player:
    return Player(name="Alice")


@pytest.fixture
def player_2() -> Player:
    return Player(name="Bob")


@pytest.fixture
def settings() -> MatchSettings:
    return MatchSettings(
        operations=[Operation.SUB],
        add_bounds=OpBounds(bounds_1=(3, 3), bounds_2=(4, 4)),
    )


def test_create_room(manager: Manager, host: Player) -> None:
    room = manager.create_room(host)

    assert room.id in manager.rooms
    assert room.host == host
    assert room.players == {host.name: host}


def test_get_room(manager: Manager, room: Room) -> None:
    assert manager.get_room(room.id) == room


def test_get_nonexistent_room(manager: Manager) -> None:
    assert manager.get_room("nonexistent") is None


def test_get_rooms(manager: Manager, player_1: Player, player_2: Player) -> None:
    room1 = manager.create_room(player_1)
    room2 = manager.create_room(player_2)

    rooms = manager.get_rooms()
    assert len(rooms) == 2
    assert room1 in rooms
    assert room2 in rooms


def test_get_rooms_empty(manager: Manager) -> None:
    assert manager.get_rooms() == []


def test_delete_room(manager: Manager, room: Room) -> None:
    assert room.id in manager.rooms

    manager.delete_room(room.id)
    assert room.id not in manager.rooms


def test_delete_nonexistent_room(manager: Manager) -> None:
    assert not manager.delete_room("nonexistent")


def test_add_player(manager: Manager, room: Room, player_1: Player) -> None:
    assert manager.add_player(room.id, player_1) == room
    assert player_1 in room.players.values()


def test_add_player_nonexistent_room(manager: Manager, player_1: Player) -> None:
    assert manager.add_player("nonexistent", player_1) is None


def test_add_player_player_already_in(
    manager: Manager, room: Room, player_1: Player
) -> None:
    assert manager.add_player(room.id, player_1) == room
    assert manager.add_player(room.id, player_1) is None


def test_remove_player(manager: Manager, room: Room, player_1: Player) -> None:
    manager.add_player(room.id, player_1)

    assert manager.remove_player(room.id, player_1) is True
    assert player_1.name not in room.players

    assert room.id in manager.rooms


def test_remove_player_last_player(manager: Manager, room: Room, host: Player) -> None:
    assert manager.remove_player(room.id, host) is True
    assert host.name not in room.players
    assert room.id not in manager.rooms


def test_remove_player_nonexistent_room(manager: Manager, player_1: Player) -> None:
    assert manager.remove_player("nonexistent", player_1) is False


def test_remove_player_player_not_in(
    manager: Manager, room: Room, player_1: Player
) -> None:
    assert manager.remove_player(room.id, player_1) is False


def test_update_settings(manager: Manager, room: Room, settings: MatchSettings) -> None:
    assert manager.update_settings(room.id, settings) is True
    assert room.match_settings == settings


def test_update_settings_nonexistent_room(
    manager: Manager, settings: MatchSettings
) -> None:
    assert manager.update_settings("nonexistent", settings) is False


def test_start_match(manager: Manager, room: Room) -> None:
    assert manager.start_match(room.id) is True


def test_start_match_nonexistent_room(manager: Manager) -> None:
    assert manager.start_match("nonexistent") is False


def test_start_match_already_started(manager: Manager, room: Room) -> None:
    manager.start_match(room.id)
    assert manager.start_match(room.id) is False


def test_end_match(manager: Manager, room: Room) -> None:
    manager.start_match(room.id)
    assert manager.end_match(room.id) is True


def test_end_match_nonexistent_room(manager: Manager) -> None:
    assert manager.end_match("nonexistent") is False


def test_end_match_already_ended(manager: Manager, room: Room) -> None:
    manager.start_match(room.id)
    manager.end_match(room.id)
    assert manager.end_match(room.id) is False


def test_handle_answer_correct(manager: Manager, room: Room, host: Player) -> None:
    manager.start_match(room.id)
    assert manager.handle_answer(room.id, host, 3) is True


def test_handle_answer_incorrect(manager: Manager, room: Room, host: Player) -> None:
    manager.start_match(room.id)
    assert manager.handle_answer(room.id, host, 0) is False


def test_handle_answer_nonexistent_room(manager: Manager, host: Player) -> None:
    assert manager.handle_answer("nonexistent", host, 0) is None


def test_handle_answer_nonexistent_match(
    manager: Manager, room: Room, host: Player
) -> None:
    assert manager.handle_answer(room.id, host, 0) is None


def test_handle_answer_nonexistent_player(
    manager: Manager, room: Room, player_1: Player
) -> None:
    manager.start_match(room.id)
    assert manager.handle_answer(room.id, player_1, 0) is None
