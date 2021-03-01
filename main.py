from Game import Game
import DiscordConnection

game = Game()
game.init_maze()

DiscordConnection.run(game)
