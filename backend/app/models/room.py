"""
Represents rooms where players join and matches take place.
"""

from pydantic import BaseModel

from app.models.match import Match, MatchSettings
from app.models.player import Player


class Room(BaseModel):
    """
    Represents a room where players join and matches take place.
    """

    id: str
    host: Player | None
    players: list[Player] = []
    match_settings: MatchSettings = MatchSettings()
    current_match: Match | None = None

    def add_player(self, player: Player) -> bool:
        """
        Adds a player to the room.

        Args:
            player: The player to add.

        Returns:
            bool: True if the player was added, False if they were already in
                  the room.
        """
        if player in self.players:
            return False

        self.players.append(player)
        return True

    def remove_player(self, player: Player) -> bool:
        """
        Removes a player from the room. If the player removed was the host,
        the first player in the list is promoted. If the room becomes empty,
        the host is set to None.

        Args:
            player: The player to remove.

        Returns:
            bool: True if the player was removed, False if they were not in
                  the room.
        """
        if player not in self.players:
            return False

        self.players.remove(player)
        if player == self.host:
            self.host = self.players[0] if self.players else None

        return True

    def update_settings(self, settings: MatchSettings) -> None:
        """
        Updates the match settings for the room to take effect on the coming
        matches.

        Args:
            settings: The settings to apply.
        """
        self.match_settings = settings

    def start_match(self) -> bool:
        """
        Starts a match in the room with the current list of players and match
        settings.

        Returns:
            bool: True if the match was started successfully, False if there
                  is already a match in progress.
        """
        if self.current_match:
            return False

        self.current_match = Match(players=self.players, settings=self.match_settings)
        self.current_match.start_match()
        return True

    def end_match(self) -> bool:
        """
        Ends the current match in the room.

        Returns:
            bool: True if the match was ended successfully, False if there
                  was no match in progress.
        """
        if not self.current_match:
            return False

        self.current_match.end_match()
        self.current_match = None
        return True
