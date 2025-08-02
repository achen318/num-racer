from enum import Enum
from typing import List, Tuple, Optional
import time

from backend.game import logic


class Operation(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"


class OpBounds:
    def __init__(self, bounds_1: Tuple[int, int], bounds_2: Tuple[int, int]):
        self.bounds_1 = bounds_1
        self.bounds_2 = bounds_2
    
    def __repr__(self) -> str:
        return f"{{{self.bounds_1} x {self.bounds_2}}}"


class Player:
    def __init__(self, name: str):
        self.name = name
        self.score = 0
        self.current_problem: Optional[Problem] = None

    def __repr__(self) -> str:
        return f"{self.name} ({self.score}) - {self.current_problem})"

    def check(self, answer: int) -> bool:
        if self.current_problem and answer == self.current_problem.result:
            self.score += 1
            return True
        return False


class Game:
    def __init__(
        self,
        players: List[Player],
        operations: List[Operation],
        add_bounds: OpBounds,  # [min, max] for add & sub
        mul_bounds: OpBounds,  # [min, max] for mul & div
        duration: int,  # total duration in seconds
    ):
        self.players = players
        self.operations = operations
        self.add_bounds = add_bounds
        self.mul_bounds = mul_bounds
        self.duration = duration

        self.active = False

    def run_game(self):
        self.active = True
        # coroutines
        end_time = time.time() + self.duration

        # Generate first problem for everybody!
        while time.time() < end_time:
            for player in self.players:
                if player.current_problem is None or player.check(5):
                    player.current_problem = logic.generate_problem(self.operations, self.add_bounds, self.mul_bounds)
        
        self.active = False
        # When it sends the first problem, start timer!
        # Javascript listener thing, will call check function each time that the input box is updated by a player.
        
    def __repr__(self) -> str:
        return f"Game(players={self.players}, operations={self.operations}, add_bounds={self.add_bounds}, mul_bounds={self.mul_bounds}, duration={self.duration})"


class Problem:
    def __init__(self, operation: Operation, num1: int, num2: int, result: int):
        self.operation = operation
        self.num1 = num1
        self.num2 = num2
        self.result = result

    def __repr__(self) -> str:
        return f"{self.num1} {self.operation.value} {self.num2} = {self.result}"
