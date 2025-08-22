import pytest
from app.models.player import Player
from app.models.problem import Operation, Problem


@pytest.fixture
def player() -> Player:
    return Player(name="Test Player")


@pytest.fixture
def problem() -> Problem:
    return Problem(num1=1, num2=1, operation=Operation.ADD, result=2)


def test_assign_problem(player: Player, problem: Problem) -> None:
    assert player.current_problem is None

    player.assign_problem(problem)
    assert player.current_problem == problem


def test_clear_problem(player: Player, problem: Problem) -> None:
    player.assign_problem(problem)
    assert player.current_problem == problem

    player.clear_problem()
    assert player.current_problem is None


def test_check_incorrect(player: Player, problem: Problem) -> None:
    assert player.score == 0

    player.assign_problem(problem)
    assert not player.check(3)
    assert player.score == 0


def test_check_correct(player: Player, problem: Problem) -> None:
    assert player.score == 0

    player.assign_problem(problem)
    assert player.check(2)
    assert player.score == 1


def test_check_multiple(player: Player, problem: Problem) -> None:
    assert player.score == 0

    player.assign_problem(problem)
    assert not player.check(3)
    assert player.score == 0

    assert player.check(2)
    assert player.score == 1

    assert not player.check(1)
    assert player.score == 1

    assert player.check(2)
    assert player.score == 2
