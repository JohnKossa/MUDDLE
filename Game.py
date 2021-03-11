import asyncio
import inspect
import random

from game_objects.Maze.Maze import Maze
from utils.Scheduler import Scheduler


class Game:
    def __init__(self):
        self.maze = None
        self.players = []
        self.discord_users = []
        self.hooks = {}
        self.aioloop = asyncio.get_event_loop()
        self.scheduler = Scheduler(self.aioloop)
        self.discord_connection = None

    def init_maze(self, width=11, height=11, difficulty=6):
        self.maze = Maze(width=width, height=height)
        self.maze.generate_maze((random.randrange(1, width - 1), width - 1), (random.randrange(1, width - 1), 0), difficulty=difficulty)

    def register_player(self, new_player):
        new_player.current_room = self.maze.entry_room
        self.players.append(new_player)

    def on(self, event, trigger_func):
        if event not in self.hooks:
            self.hooks[event] = []
        self.hooks[event].append(trigger_func)

    def off(self, event, trigger_func):
        if event in self.hooks and trigger_func in self.hooks[event]:
            self.hooks[event].remove(trigger_func)
            if len(self.hooks[event]) == 0:
                del self.hooks[event]
            return True
        return False

    def trigger(self, event, *args, **kwargs):
        # TODO join args with f_args and kwargs with f_kwargs before passing
        if event in self.hooks:
            for trigger_func in self.hooks[event]:
                if inspect.iscoroutine(trigger_func):
                    self.aioloop.create_task(trigger_func.func(*trigger_func.f_args, **trigger_func.f_kwargs))
                else:
                    trigger_func.func(*trigger_func.f_args, **trigger_func.f_kwargs)


class TriggerFunc:
    def __init__(self, func, *f_args, **f_kwargs):
        self.func = func
        self.f_args = f_args
        self.f_kwargs = f_kwargs
