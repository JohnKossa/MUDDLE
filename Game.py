import random

from game_objects.Maze import Maze


class Game:
    def __init__(self):
        self.maze = None
        self.players = []
        self.discord_users = []

    def init_maze(self, width=11, height=11, difficulty=6):
        self.maze = Maze(width=width, height=height, entry_coords=(random.randrange(1, width - 1), width - 1),
                         exit_coords=(random.randrange(1, width - 1), 0))
        self.maze.generate_maze(difficulty=difficulty)

    def register_player(self, new_player):
        new_player.current_room = self.maze.entry_room
        self.players.append(new_player)

    def generate_command_list(self, player):
        # generate a list of all possible commands
        # commands can come from:
        #   the room
        #   room fixtures
        #   player equipment
        #   player skills
        #   player active effects
        pass
