"""
Represents matches that occur in a room.
"""

import random

from app.models.player import Player
from app.models.problem import OpBounds, Operation, Problem
from pydantic import BaseModel


class MatchSettings(BaseModel):
    """
    Represents the settings for a match, with allowed operations,
    addition/subtraction bounds, multiplication/division bounds, and a
    duration in seconds.
    """

    operations: list[Operation] = list(Operation)
    add_bounds: OpBounds = OpBounds(bounds_1=(2, 100), bounds_2=(2, 100))
    mul_bounds: OpBounds = OpBounds(bounds_1=(2, 12), bounds_2=(2, 100))
    duration: int = 120


class MatchResult(BaseModel):
    """
    Represents the result of a match, including the winner and final scores.

    Final scores are captured in a dictionary mapping player names to their
    score.
    """

    winner: Player
    final_scores: dict[str, int] = {}


class Match(BaseModel):
    """
    Represents a match that occurs in a room.
    """

    players: dict[str, Player] = {}
    settings: MatchSettings = MatchSettings()
    active: bool = False
    result: MatchResult | None = None

    def _generate_problem(self) -> Problem:
        """
        Generates a new problem based on the current settings.
        """
        return Problem.generate(
            random.choice(self.settings.operations),
            self.settings.add_bounds,
            self.settings.mul_bounds,
        )

    def start_match(self) -> None:
        """
        Starts the match and assigns a new problem to each player.

        Raises:
            ValueError: If the operations list is empty.
        """
        if not self.settings.operations:
            raise ValueError("No operations available to generate problems.")

        self.active = True

        for player in self.players.values():
            player.assign_problem(self._generate_problem())

    def end_match(self) -> None:
        """
        Ends the match, clears each player's problem, and updates the match
        result.
        """
        self.active = False

        for player in self.players.values():
            player.clear_problem()

        self.result = MatchResult(
            winner=max(self.players.values(), key=lambda p: p.score),
            final_scores={
                player.name: player.score for player in self.players.values()
            },
        )

    def handle_answer(self, player: Player, answer: int) -> bool:
        """
        Handles a player's answer to a question in the match by checking the
        answer and assigning a new problem if the answer is correct.

        Args:
            player: The player submitting the answer.
            answer: The answer submitted by the player.

        Returns:
            True if the answer was correct, False if the answer was incorrect
            or the player does not exist.
        """
        if player.name in self.players and player.check(answer):
            player.assign_problem(self._generate_problem())
            return True

        return False
