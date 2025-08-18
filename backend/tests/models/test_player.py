import pytest
from app.models.player import Player
from app.models.problem import Operation, Problem


@pytest.fixture
def player() -> Player:
    return Player(name="Test Player")


@pytest.fixture
def problem_1() -> Problem:
    return Problem(num1=1, num2=1, operation=Operation.ADD, result=2)


@pytest.fixture
def problem_2() -> Problem:
    return Problem(num1=2, num2=2, operation=Operation.ADD, result=4)


def test_assign_problem(player: Player, problem_1: Problem) -> None:
    assert player.current_problem is None

    player.assign_problem(problem_1)
    assert player.current_problem == problem_1


def test_assign_problems(
    player: Player, problem_1: Problem, problem_2: Problem
) -> None:
    assert player.current_problem is None

    player.assign_problem(problem_1)
    assert player.current_problem == problem_1

    player.assign_problem(problem_2)
    assert player.current_problem == problem_2


def test_check_incorrect(player: Player, problem_1: Problem) -> None:
    assert player.score == 0

    player.assign_problem(problem_1)
    assert not player.check(3)
    assert player.score == 0


def test_check_correct(player: Player, problem_1: Problem) -> None:
    assert player.score == 0

    player.assign_problem(problem_1)
    assert player.check(2)
    assert player.score == 1


def test_check_multiple(player: Player, problem_1: Problem) -> None:
    assert player.score == 0

    player.assign_problem(problem_1)
    assert not player.check(3)
    assert player.score == 0

    assert player.check(2)
    assert player.score == 1

    assert not player.check(1)
    assert player.score == 1

    assert player.check(2)
    assert player.score == 2
