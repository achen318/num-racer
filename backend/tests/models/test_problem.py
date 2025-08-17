import pytest
from app.models.problem import Problem, Operation, OpBounds

LOWER = 1
UPPER = 10


@pytest.fixture
def bounds():
    assert LOWER <= UPPER
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
    assert LOWER <= problem.num2 <= UPPER
    assert LOWER <= problem.result <= UPPER
    assert problem.result == problem.num1 - problem.num2


def test_generate_mul(bounds: OpBounds):
    problem = Problem.generate(Operation.MUL, bounds)

    assert problem.operation == Operation.MUL
    assert LOWER <= problem.num1 <= UPPER
    assert LOWER <= problem.num2 <= UPPER
    assert problem.result == problem.num1 * problem.num2


def test_generate_div(bounds: OpBounds):
    problem = Problem.generate(Operation.DIV, bounds)

    assert problem.operation == Operation.DIV
    assert LOWER <= problem.num2 <= UPPER
    assert LOWER <= problem.result <= UPPER
    assert problem.num2 != 0
    assert problem.result == problem.num1 / problem.num2


def test_invalid_bounds_1():
    assert LOWER <= UPPER
    bounds = OpBounds(bounds_1=(UPPER, LOWER), bounds_2=(LOWER, UPPER))

    with pytest.raises(ValueError):
        Problem.generate(Operation.ADD, bounds)

    with pytest.raises(ValueError):
        Problem.generate(Operation.SUB, bounds)

    with pytest.raises(ValueError):
        Problem.generate(Operation.MUL, bounds)

    with pytest.raises(ValueError):
        Problem.generate(Operation.DIV, bounds)


def test_invalid_bounds_2():
    assert LOWER <= UPPER
    bounds = OpBounds(bounds_1=(LOWER, UPPER), bounds_2=(UPPER, LOWER))

    with pytest.raises(ValueError):
        Problem.generate(Operation.ADD, bounds)

    with pytest.raises(ValueError):
        Problem.generate(Operation.SUB, bounds)

    with pytest.raises(ValueError):
        Problem.generate(Operation.MUL, bounds)

    with pytest.raises(ValueError):
        Problem.generate(Operation.DIV, bounds)


def test_div_by_zero():
    assert LOWER <= UPPER
    bounds = OpBounds(bounds_1=(0, 0), bounds_2=(LOWER, UPPER))

    with pytest.raises(ValueError):
        Problem.generate(Operation.DIV, bounds)


def test_potential_div_by_zero():
    assert LOWER <= UPPER
    bounds = OpBounds(bounds_1=(0, 1), bounds_2=(LOWER, UPPER))

    problem = Problem.generate(Operation.DIV, bounds)
    assert problem.num2 != 0
