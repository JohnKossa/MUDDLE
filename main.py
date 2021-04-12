from Game import Game
import DiscordConnection

game = Game()
game.init_maze()
game.setup_hooks()

DiscordConnection.run(game)
