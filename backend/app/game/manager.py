import app.game.logic as logic
from app.game.state import Player, Game, Problem


class Manager:
    def __init__(self):
        self.rooms = []
        self.room_dict: dict[int, Game] = {}
        self.player_dict: dict[str, Player] = {}

    def get_player(self, player_id: str) -> Player | None:
        """
        This method will be used by the API to associate an ID for each
        websocket connection to a player object.
        """
        return self.player_dict.get(player_id, None)

    def create_room(self, host: Player):
        room_id = len(self.rooms) + 1

        self.room_dict[room_id] = Game(host, [])
        self.room_dict[room_id].host = host
        return self.room_dict[room_id]

    def add_player(self, room_id, player: Player):
        self.room_dict[room_id].players.append(player)

    def remove_player(self, room_id, player: Player):
        if player in self.room_dict[room_id].players:
            self.room_dict[room_id].players.remove(player)
        else:
            raise ValueError("Player not found in the room")

    def list_players(self, room_id):
        return [player.name for player in self.room_dict[room_id].players]

    def start_game(self, room_id):
        self.room_dict[room_id].active = True

    def end_game(self, room_id):
        self.room_dict[room_id].active = False
        for player in self.room_dict[room_id].players:
            player.current_problem = None

    def reset_game(self, room_id):
        for player in self.room_dict[room_id].players:
            player.score = 0
            player.current_problem = None

    def generate_question(self, room_id):
        problem = logic.generate_problem(
            self.room_dict[room_id].operations,
            self.room_dict[room_id].add_bounds,
            self.room_dict[room_id].mul_bounds,
        )
        return problem

    def submit_answer(self, room_id, player: Player, answer):
        if player.current_problem is None:
            raise ValueError("No active problem for the player")
        if answer == player.current_problem.answer:
            self.update_score(room_id, player)
            player.current_problem = self.generate_question(room_id)

    def update_score(self, room_id, player: Player):
        player.score += 1


manager = Manager()
