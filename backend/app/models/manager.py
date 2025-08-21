from app.models.player import Player
from app.models.room import Room
from pydantic import BaseModel


class Manager(BaseModel):
    """
    Represents a room manager that handles room operations from the server.
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
        room = Room(id=room_id, host=host)
        self.rooms[room_id] = room
        return room

    def delete_room(self, room_id: str) -> None:
        """
        Deletes the room with the given ID.

        Args:
            room_id: The ID of the room to delete.
        """
        self.rooms.pop(room_id, None)

    def join_room(self, room_id: str, player: Player) -> Room | None:
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

    def leave_room(self, room_id: str, player: Player) -> Room | None:
        """
        Removes a player from the room with the given ID.

        Args:
            room_id: The ID of the room to leave.
            player: The player to remove from the room.

        Returns:
            The Room object that the player left, or None if the leave failed
            because the room does not exist or the player could not be removed.
        """
        if room := self.get_room(room_id):
            if room.remove_player(player):
                return room

        return None

    def start_match(self, room_id: str) -> bool:
        """
        Starts the match in the room with the given ID.

        Args:
            room_id: The ID of the room to start the match in.

        Returns:
            True if the match was started successfully, False otherwise.
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
            True if the match was ended successfully, False otherwise.
        """
        if room := self.get_room(room_id):
            return room.end_match()
        return False

    def handle_answer(self, room_id: str, player: Player, answer: int) -> bool:
        """
        Handles a player's answer to a question in the room.

        Args:
            room_id: The ID of the room the player is in.
            player: The player submitting the answer.
            answer: The answer submitted by the player.

        Returns:
            True if the answer was correct, False if the answer was incorrect
            or the room/player does not exist.
        """
        if room := self.get_room(room_id):
            if plr := room.players.get(player.name):
                return plr.check(answer)

        return False
