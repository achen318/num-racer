import pytest
from app.models.problem import Problem, Operation, OpBounds

LOWER = 1
UPPER = 10


@pytest.fixture
def bounds():
    return OpBounds(bounds_1=(LOWER, UPPER), bounds_2=(LOWER, UPPER))


def test_generate_add(bounds: OpBounds):
    problem = Problem.generate(Operation.ADD, bounds)

    assert problem.operation == Operation.ADD
    assert LOWER <= problem.num1 <= UPPER
    assert LOWER <= problem.num2 <= UPPER
    assert problem.result == problem.num1 + problem.num2


def test_generate_sub(bounds: OpBounds):
    problem = Problem.generate(Operation.SUB, bounds)

    assert problem.operation == Operation.SUB
    assert problem.result == problem.num1 - problem.num2
    assert problem.result >= 0


def test_generate_mul(bounds: OpBounds):
    problem = Problem.generate(Operation.MUL, bounds)

    assert problem.operation == Operation.MUL
    assert LOWER <= problem.num1 <= UPPER
    assert LOWER <= problem.num2 <= UPPER
    assert problem.result == problem.num1 * problem.num2


def test_generate_div(bounds: OpBounds):
    problem = Problem.generate(Operation.DIV, bounds)

    assert problem.operation == Operation.DIV
    assert problem.num2 != 0
    assert problem.result == problem.num1 / problem.num2
