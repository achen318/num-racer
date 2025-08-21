"""
Represents matches that occur in a room.
"""

from app.models.player import Player
from app.models.problem import OpBounds, Operation
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
    active: bool = True
    result: MatchResult | None = None

    def start_match(self) -> None:
        """
        Starts the match.
        """
        self.active = True

    def end_match(self) -> None:
        """
        Ends the match and updates the match result.
        """
        self.active = False

        self.result = MatchResult(
            winner=max(self.players.values(), key=lambda p: p.score),
            final_scores={
                player.name: player.score for player in self.players.values()
            },
        )
