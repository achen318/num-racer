import app.game.logic


class Player:
    def __init__(self, name: str):
        self.name = name
        self.score = 0
        self.current_problem: Problem | None = None

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
        host: Player,
        players: list[Player],
        operations: list[Operation] | None = None,
        add_bounds: OpBounds = OpBounds((2, 100), (2, 100)),  # [min, max] for add & sub
        mul_bounds: OpBounds = OpBounds((2, 12), (2, 100)),  # [min, max] for mul & div
        duration: int = 120,  # total duration in seconds
    ):
        if operations is None:
            operations = [
                Operation.ADD,
                Operation.SUB,
                Operation.MUL,
                Operation.DIV,
            ]

        self.players = players
        self.host = host
        self.operations = operations
        self.add_bounds = add_bounds
        self.mul_bounds = mul_bounds
        self.duration = duration

        self.active = False

    def __repr__(self) -> str:
        return f"""Game(players={self.players},
          operations={self.operations},
            add_bounds={self.add_bounds},
              mul_bounds={self.mul_bounds},
                duration={self.duration})"""
