from models import Problem, Operation, OpBounds

import random
from typing import List


def generate_problem(
    operations: List[Operation],
    add_bounds: OpBounds,
    mul_bounds: OpBounds,
) -> Problem:
    operation = random.choice(operations)
    if operation == Operation.ADD:
        return add(add_bounds)
    elif operation == Operation.SUB:
        return sub(add_bounds)
    elif operation == Operation.MUL:
        return mul(mul_bounds)
    else:
        return div(mul_bounds)


def add(add_bounds: OpBounds) -> Problem:
    a = random.randint(add_bounds.bounds_1[0], add_bounds.bounds_1[1])
    b = random.randint(add_bounds.bounds_1[0], add_bounds.bounds_1[1])
    return Problem(Operation.ADD, a, b, a + b)


def sub(add_bounds: OpBounds) -> Problem:
    add_problem = add(add_bounds)
    return Problem(
        Operation.SUB, add_problem.result, add_problem.num1, add_problem.num2
    )


def mul(mul_bounds: OpBounds) -> Problem:
    a = random.randint(mul_bounds.bounds_1[0], mul_bounds.bounds_1[1])
    b = random.randint(mul_bounds.bounds_2[0], mul_bounds.bounds_2[1])
    return Problem(Operation.MUL, a, b, a * b)


def div(mul_bounds: OpBounds) -> Problem:
    mul_problem = mul(mul_bounds)
    return Problem(
        Operation.DIV, mul_problem.result, mul_problem.num1, mul_problem.num2
    )
