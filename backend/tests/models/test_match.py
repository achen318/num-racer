import pytest
from app.models.match import Match, MatchResult
from app.models.player import Player


@pytest.fixture
def match() -> Match:
    return Match(
        players={
            "Alice": Player(name="Alice"),
            "Bob": Player(name="Bob"),
            "Charlie": Player(name="Charlie"),
        }
    )


def test_start_match(match: Match) -> None:
    match.start_match()
    assert match.active is True


def test_end_match(match: Match) -> None:
    match.end_match()
    assert match.active is False


def test_results(match: Match) -> None:
    match.players["Alice"].score = 10
    match.players["Bob"].score = 20
    match.players["Charlie"].score = 15

    match.end_match()

    assert isinstance(match.result, MatchResult)
    assert match.result.winner.name == "Bob"
    assert match.result.final_scores == {
        "Alice": 10,
        "Bob": 20,
        "Charlie": 15,
    }
