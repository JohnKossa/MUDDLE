import random

from game_objects.Maze.Maze import Maze


class Game:
    def __init__(self):
        self.maze = None
        self.players = []
        self.discord_users = []

    def init_maze(self, width=11, height=11, difficulty=6):
        self.maze = Maze(width=width, height=height)
        self.maze.generate_maze((random.randrange(1, width - 1), width - 1), (random.randrange(1, width - 1), 0), difficulty=difficulty)

    def register_player(self, new_player):
        new_player.current_room = self.maze.entry_room
        self.players.append(new_player)
