import pytest
from app.models.match import Match, MatchResult
from app.models.player import Player


@pytest.fixture
def match():
    return Match(
        players=[
            Player(name="Alice"),
            Player(name="Bob"),
            Player(name="Charlie"),
        ]
    )


def test_start_match(match):
    match.start_match()
    assert match.active is True


def test_end_match(match):
    match.end_match()
    assert match.active is False


def test_results(match):
    match.players[0].score = 10
    match.players[1].score = 20
    match.players[2].score = 15

    match.end_match()

    assert isinstance(match.result, MatchResult)
    assert match.result.winner.name == "Bob"
    assert match.result.final_scores == {
        "Alice": 10,
        "Bob": 20,
        "Charlie": 15,
    }
