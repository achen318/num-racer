import pytest
from app.models.match import MatchSettings
from app.models.player import Player
from app.models.problem import OpBounds, Operation
from app.models.room import Room


@pytest.fixture
def room() -> Room:
    host = Player(name="Host")
    return Room(id="test", host=host, players={"Host": host})


@pytest.fixture
def player_1() -> Player:
    return Player(name="Alice")


@pytest.fixture
def player_2() -> Player:
    return Player(name="Bob")


@pytest.fixture
def settings() -> MatchSettings:
    return MatchSettings(
        operations=[Operation.ADD, Operation.SUB],
        add_bounds=OpBounds(bounds_1=(1, 2), bounds_2=(3, 4)),
        mul_bounds=OpBounds(bounds_1=(5, 6), bounds_2=(7, 8)),
        duration=60,
    )


def test_add_player(room: Room, player_1: Player) -> None:
    assert player_1.name not in room.players
    assert room.add_player(player_1)
    assert player_1.name in room.players


def test_add_existing_player(room: Room, player_1: Player) -> None:
    assert player_1.name not in room.players

    assert room.add_player(player_1)
    assert player_1.name in room.players

    assert not room.add_player(player_1)
    assert player_1.name in room.players


def test_remove_player(room: Room, player_1: Player) -> None:
    room.add_player(player_1)
    assert player_1.name in room.players

    assert room.remove_player(player_1)
    assert player_1.name not in room.players


def test_remove_nonexistent_player(room: Room, player_1: Player) -> None:
    assert player_1.name not in room.players

    assert not room.remove_player(player_1)
    assert player_1.name not in room.players


def test_remove_host_and_promote(
    room: Room, player_1: Player, player_2: Player
) -> None:
    room.add_player(player_1)
    room.add_player(player_2)

    assert room.host == room.players["Host"]

    assert room.remove_player(room.players["Host"])
    assert room.host == player_1
    assert room.host != player_2


def test_remove_host_and_delete(room: Room) -> None:
    assert room.host == room.players["Host"]
    assert room.remove_player(room.players["Host"])
    assert room.host is None
    assert len(room.players) == 0


def test_update_settings(room: Room, settings: MatchSettings) -> None:
    assert room.match_settings != settings
    room.update_settings(settings)
    assert room.match_settings == settings


def test_start_match(room: Room) -> None:
    assert room.current_match is None
    assert room.start_match()
    assert room.current_match is not None


def test_start_match_in_progress(room: Room) -> None:
    assert room.current_match is None
    assert room.start_match()

    assert not room.start_match()
    assert room.current_match is not None


def test_end_match(room: Room) -> None:
    assert room.current_match is None
    assert room.start_match()
    assert room.current_match is not None

    assert room.end_match()
    assert room.current_match is None


def test_end_match_nonexistent(room: Room) -> None:
    assert room.current_match is None
    assert not room.end_match()
    assert room.current_match is None
