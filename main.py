from Game import Game
from game_objects.Player import Player
import DiscordConnection

game = Game()
game.init_maze()
p1 = Player()
game.register_player(p1)
p1.current_room = game.maze.entry_room

DiscordConnection.run(game)
