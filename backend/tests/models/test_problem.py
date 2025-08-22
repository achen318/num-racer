import pytest
from app.models.problem import OpBounds, Operation, Problem

A_LOWER = 11
A_UPPER = 20

M_LOWER = 1
M_UPPER = 10


@pytest.fixture
def add_bounds() -> OpBounds:
    assert A_LOWER <= A_UPPER
    return OpBounds(bounds_1=(A_LOWER, A_UPPER), bounds_2=(A_LOWER, A_UPPER))


@pytest.fixture
def mul_bounds() -> OpBounds:
    assert M_LOWER <= M_UPPER
    return OpBounds(bounds_1=(M_LOWER, M_UPPER), bounds_2=(M_LOWER, M_UPPER))


def test_generate_add(add_bounds: OpBounds, mul_bounds: OpBounds) -> None:
    problem = Problem.generate(Operation.ADD, add_bounds, mul_bounds)

    assert problem.operation == Operation.ADD
    assert A_LOWER <= problem.num1 <= A_UPPER
    assert A_LOWER <= problem.num2 <= A_UPPER
    assert problem.result == problem.num1 + problem.num2


def test_generate_sub(add_bounds: OpBounds, mul_bounds: OpBounds) -> None:
    problem = Problem.generate(Operation.SUB, add_bounds, mul_bounds)

    assert problem.operation == Operation.SUB
    assert A_LOWER <= problem.num2 <= A_UPPER
    assert A_LOWER <= problem.result <= A_UPPER
    assert problem.result == problem.num1 - problem.num2


def test_generate_mul(add_bounds: OpBounds, mul_bounds: OpBounds) -> None:
    problem = Problem.generate(Operation.MUL, add_bounds, mul_bounds)

    assert problem.operation == Operation.MUL
    assert M_LOWER <= problem.num1 <= M_UPPER
    assert M_LOWER <= problem.num2 <= M_UPPER
    assert problem.result == problem.num1 * problem.num2


def test_generate_div(add_bounds: OpBounds, mul_bounds: OpBounds) -> None:
    problem = Problem.generate(Operation.DIV, add_bounds, mul_bounds)

    assert problem.operation == Operation.DIV
    assert M_LOWER <= problem.num2 <= M_UPPER
    assert M_LOWER <= problem.result <= M_UPPER
    assert problem.num2 != 0
    assert problem.result == problem.num1 / problem.num2


def test_invalid_bounds_1() -> None:
    assert A_LOWER <= A_UPPER
    add_bounds = OpBounds(bounds_1=(A_UPPER, A_LOWER), bounds_2=(A_LOWER, A_UPPER))

    assert M_LOWER <= M_UPPER
    mul_bounds = OpBounds(bounds_1=(M_UPPER, M_LOWER), bounds_2=(M_LOWER, M_UPPER))

    with pytest.raises(ValueError):
        Problem.generate(Operation.ADD, add_bounds, mul_bounds)

    with pytest.raises(ValueError):
        Problem.generate(Operation.SUB, add_bounds, mul_bounds)

    with pytest.raises(ValueError):
        Problem.generate(Operation.MUL, add_bounds, mul_bounds)

    with pytest.raises(ValueError):
        Problem.generate(Operation.DIV, add_bounds, mul_bounds)


def test_invalid_bounds_2() -> None:
    assert A_LOWER <= A_UPPER
    add_bounds = OpBounds(bounds_1=(A_LOWER, A_UPPER), bounds_2=(A_UPPER, A_LOWER))

    assert M_LOWER <= M_UPPER
    mul_bounds = OpBounds(bounds_1=(M_LOWER, M_UPPER), bounds_2=(M_UPPER, M_LOWER))

    with pytest.raises(ValueError):
        Problem.generate(Operation.ADD, add_bounds, mul_bounds)

    with pytest.raises(ValueError):
        Problem.generate(Operation.SUB, add_bounds, mul_bounds)

    with pytest.raises(ValueError):
        Problem.generate(Operation.MUL, add_bounds, mul_bounds)

    with pytest.raises(ValueError):
        Problem.generate(Operation.DIV, add_bounds, mul_bounds)


def test_div_by_zero(add_bounds: OpBounds) -> None:
    assert M_LOWER <= M_UPPER
    mul_bounds = OpBounds(bounds_1=(0, 0), bounds_2=(M_LOWER, M_UPPER))

    with pytest.raises(ValueError):
        Problem.generate(Operation.DIV, add_bounds, mul_bounds)


def test_potential_div_by_zero(add_bounds: OpBounds) -> None:
    assert M_LOWER <= M_UPPER
    mul_bounds = OpBounds(bounds_1=(0, 1), bounds_2=(M_LOWER, M_UPPER))

    problem = Problem.generate(Operation.DIV, add_bounds, mul_bounds)
    assert problem.num2 != 0
