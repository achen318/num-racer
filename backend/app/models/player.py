"""
Represents players in a match.
"""

from app.models.problem import Problem
from pydantic import BaseModel


class Player(BaseModel):
    """
    Represents a player in a match.
    """

    name: str
    score: int = 0
    current_problem: Problem | None = None

    def __str__(self) -> str:
        return f"{self.name} ({self.score}) - {self.current_problem}"

    def check(self, answer: int) -> bool:
        """
        Checks if the given answer is correct for the current problem. Grants
        a point to the player if the answer is correct.

        Args:
            answer: The player's answer to the current problem.

        Returns:
            bool: True if the answer is correct, False otherwise.
        """
        if self.current_problem and answer == self.current_problem.result:
            self.score += 1
            return True

        return False

    def assign_problem(self, problem: Problem) -> None:
        """
        Assigns a new problem to the player.

        Args:
            problem: The problem to assign to the player.
        """
        self.current_problem = problem
