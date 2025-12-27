"""
Represents a manager that handles game rooms and player interactions.
"""

from app.models.match import MatchSettings
from app.models.player import Player
from app.models.room import Room
from pydantic import BaseModel


class Manager(BaseModel):
    """
    Represents a manager that handles game rooms and player interactions.
    """

    rooms: dict[str, Room] = {}

    def get_room(self, room_id: str) -> Room | None:
        """
        Returns the room with the given ID, or None if it does not exist.

        Args:
            room_id: The ID of the room to retrieve.
        """
        return self.rooms.get(room_id)

    def get_rooms(self) -> list[Room]:
        """
        Returns a list of all active rooms.
        """
        return list(self.rooms.values())

    def create_room(self, host: Player) -> Room:
        """
        Creates a new room with the given player as the host.

        Args:
            host: The player to create the room to serve as the room host.

        Returns:
            A Room object representing the newly created room, with the
            default settings.
        """
        room_id = str(len(self.rooms) + 1)  # TODO: generate unique ID
        room = Room(id=room_id, host=host, players={host.name: host})
        self.rooms[room_id] = room
        return room

    def delete_room(self, room_id: str) -> bool:
        """
        Deletes the room with the given ID.

        Args:
            room_id: The ID of the room to delete.

        Returns:
            True if the room was deleted successfully, False if the room does
            not exist.
        """
        return self.rooms.pop(room_id, None) is not None

    def add_player(self, room_id: str, player: Player) -> Room | None:
        """
        Adds a player to the room with the given ID.

        Args:
            room_id: The ID of the room to join.
            player: The player to add to the room.

        Returns:
            The Room object that the player joined, or None if the join failed
            because the room does not exist or the player could not be added.
        """
        if room := self.get_room(room_id):
            if room.add_player(player):
                return room

        return None

    def remove_player(self, room_id: str, player: Player) -> bool:
        """
        Removes a player from the room with the given ID. If no more players
        remain in the room, the room is deleted.

        Args:
            room_id: The ID of the room to leave.
            player: The player to remove from the room.

        Returns:
            True if the player was removed successfully, False if the room does
            not exist or the player could not be removed.
        """
        if room := self.get_room(room_id):
            if room.remove_player(player):
                if not room.players:
                    self.delete_room(room_id)
                return True

        return False

    def update_settings(self, room_id: str, settings: MatchSettings) -> bool:
        """
        Updates the match settings for the room with the given ID.

        Args:
            room_id: The ID of the room to update.
            settings: The new match settings for the room.

        Returns:
            True if the settings were updated successfully, False if the room
            does not exist.
        """
        if room := self.get_room(room_id):
            room.update_settings(settings)
            return True

        return False

    def start_match(self, room_id: str) -> bool:
        """
        Starts the match in the room with the given ID.

        Args:
            room_id: The ID of the room to start the match in.

        Returns:
            True if the match was started successfully, False if the room does
            not exist or the match could not be started.
        """
        if room := self.get_room(room_id):
            return room.start_match()
        return False

    def end_match(self, room_id: str) -> bool:
        """
        Ends the match in the room with the given ID.

        Args:
            room_id: The ID of the room to end the match in.

        Returns:
            True if the match was ended successfully, False if the room does
            not exist or the match could not be ended.
        """
        if room := self.get_room(room_id):
            return room.end_match()
        return False

    def handle_answer(self, room_id: str, player: Player, answer: int) -> bool | None:
        """
        Handles a player's answer to a question in the match.

        Args:
            room_id: The ID of the room the player is in.
            player: The player submitting the answer.
            answer: The answer submitted by the player.

        Returns:
            True if the answer was correct, False if the answer was incorrect,
            or None if the room/match/player does not exist.
        """
        if room := self.get_room(room_id):
            if match := room.current_match:
                return match.handle_answer(player, answer)

        return None
