import pytest
from app.models.match import Match, MatchResult, MatchSettings
from app.models.player import Player
from app.models.problem import OpBounds, Operation, Problem


@pytest.fixture
def match() -> Match:
    return Match(
        players={
            "Alice": Player(name="Alice"),
            "Bob": Player(name="Bob"),
        },
        settings=MatchSettings(
            operations=[Operation.ADD],
            add_bounds=OpBounds(bounds_1=(1, 1), bounds_2=(2, 2)),
        ),
    )


@pytest.fixture
def problem() -> Problem:
    return Problem(num1=1, num2=2, operation=Operation.ADD, result=3)


def test_start_match(match: Match, problem: Problem) -> None:
    match.start_match()
    assert match.active is True
    assert all(player.current_problem == problem for player in match.players.values())


def test_start_match_bad_settings(match: Match) -> None:
    match.settings.operations = []

    with pytest.raises(ValueError):
        match.start_match()

    assert match.active is False


def test_end_match(match: Match) -> None:
    match.end_match()
    assert match.active is False
    assert all(player.current_problem is None for player in match.players.values())


def test_results(match: Match) -> None:
    match.players["Alice"].score = 10
    match.players["Bob"].score = 20

    match.end_match()

    assert isinstance(match.result, MatchResult)
    assert match.result.winner.name == "Bob"
    assert match.result.final_scores == {
        "Alice": 10,
        "Bob": 20,
    }


def test_handle_answer_correct(match: Match, problem: Problem) -> None:
    match.start_match()

    player = match.players["Alice"]
    player.current_problem = Problem(num1=3, num2=4, operation=Operation.ADD, result=7)

    assert player.score == 0

    assert match.handle_answer(player, 7) is True
    assert player.score == 1

    assert player.current_problem == problem
    assert match.handle_answer(player, 3) is True
    assert player.score == 2


def test_handle_answer_incorrect(match: Match) -> None:
    match.start_match()

    player = match.players["Alice"]
    assert player.score == 0

    assert match.handle_answer(player, 8) is False
    assert player.score == 0


def test_handle_answer_nonexistent_player(match: Match) -> None:
    match.start_match()

    nonexistent_player = Player(name="nonexistent")
    assert match.handle_answer(nonexistent_player, 5) is False
