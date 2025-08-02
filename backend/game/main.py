from models import Game, Player, Operation, OpBounds

players = [Player("Anthony"), Player("Patrick")]
operations = [Operation.ADD, Operation.SUB, Operation.MUL, Operation.DIV]
add_bounds = OpBounds((2, 100), (2, 100))
mul_bounds = OpBounds((2, 12), (2, 100))
duration = 30

game = Game(players, operations, add_bounds, mul_bounds, duration)

# game.check(players[0], 2)
# game.check(players[1], 3)

import logic
a = logic.generate_problem(operations, add_bounds, mul_bounds)
print(players)
print(a.num1, " ", a.operation, " ")

players[0].score += 1
players[1].score += 2

print(game)
