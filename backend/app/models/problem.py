"""
Represents binary arithmetic problems with two operands and an operation.
"""

import random
from enum import StrEnum

from pydantic import BaseModel


class Operation(StrEnum):
    """
    Represents the four basic arithmetic operations and their symbols.
    """

    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"


class OpBounds(BaseModel):
    """
    Represents a pair of [lower, upper] bounds for the two operands.
    """

    bounds_1: tuple[int, int]
    bounds_2: tuple[int, int]

    def __str__(self) -> str:
        return f"{{{self.bounds_1} x {self.bounds_2}}}"


class Problem(BaseModel):
    """
    Represents a binary arithmetic problem with two operands, an operation,
    and the result.
    """

    num1: int
    num2: int
    operation: Operation
    result: int

    def __str__(self) -> str:
        return f"{self.num1} {self.operation.value} {self.num2} = {self.result}"

    @classmethod
    def generate(cls, operation: Operation, add_bounds: OpBounds, mul_bounds: OpBounds):
        """
        Generates a problem with the given operation and randomly chosen
        operands within the given bounds.

        Args:
            operation: The arithmetic operation to perform.
            add_bounds: The bounds within which to generate operands for
                        addition/subtraction.
            mul_bounds: The bounds within which to generate operands for
                        multiplication/division.

        Returns:
            A Problem instance with the generated operands and operation.

        Raises:
            ValueError: If the bounds are invalid (i.e. lower > greater) or
                        equal to 0 for the divisor.
        """
        if operation == Operation.ADD:
            return cls._generate_add(add_bounds)
        if operation == Operation.SUB:
            return cls._generate_sub(add_bounds)
        if operation == Operation.MUL:
            return cls._generate_mul(mul_bounds)

        return cls._generate_div(mul_bounds)

    @classmethod
    def _generate_add(cls, bounds: OpBounds):
        a = random.randint(*bounds.bounds_1)
        b = random.randint(*bounds.bounds_2)

        return cls(
            num1=a,
            num2=b,
            operation=Operation.ADD,
            result=a + b,
        )

    @classmethod
    def _generate_sub(cls, bounds: OpBounds):
        add_problem = cls._generate_add(bounds)

        return cls(
            num1=add_problem.result,
            num2=add_problem.num1,
            operation=Operation.SUB,
            result=add_problem.num2,
        )

    @classmethod
    def _generate_mul(cls, bounds: OpBounds):
        a = random.randint(*bounds.bounds_1)
        b = random.randint(*bounds.bounds_2)

        return cls(
            num1=a,
            num2=b,
            operation=Operation.MUL,
            result=a * b,
        )

    @classmethod
    def _generate_div(cls, bounds: OpBounds):
        if bounds.bounds_1 == (0, 0):
            raise ValueError("Divisor cannot have the range [0, 0].")

        while mul_problem := cls._generate_mul(bounds):
            if mul_problem.num1 != 0:
                break

        return cls(
            num1=mul_problem.result,
            num2=mul_problem.num1,
            operation=Operation.DIV,
            result=mul_problem.num2,
        )
