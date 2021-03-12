import asyncio
import inspect
import math
import random

from discord_objects.DiscordUser import DiscordUser, UserUtils
from game_objects.Enemy import Enemy
from game_objects.Maze.Maze import Maze
from game_objects.Maze.MazeRoom import RoomUtils
from utils.Scheduler import Scheduler


class Game:
    def __init__(self):
        self.maze = None
        self.players = []
        self.enemies = []
        self.discord_users = []
        self.hooks = {}
        self.aioloop = asyncio.get_event_loop()
        self.scheduler = Scheduler(self.aioloop)
        self.discord_connection = None

    def setup_hooks(self):
        self.on("enter_room", TriggerFunc(self.start_combat))

    def seed_enemies(self):
        num_enemies = math.isqrt(self.maze.width * self.maze.height)
        viable_rooms = list(filter(lambda x: x != self.maze.entry_room and x != self.maze.exit_room, self.maze.rooms))
        chosen_rooms = random.choices(viable_rooms, k=num_enemies)
        for room in chosen_rooms:
            new_enemy = Enemy()
            new_enemy.current_room = room
            new_enemy.name = "Goblin"
            self.enemies.append(new_enemy)

    def start_combat(self, room=None, **kwargs):
        if room is None:
            return
        if len(room.get_enemies(self)) > 0 and len(room.get_players(self)) > 0:
            room.start_combat(self)

    def check_final_room(self, room=None, source_player=None):
        if room == self.maze.exit_room:
            UserUtils.get_user_by_character_name(source_player, self.discord_users)
            self.discord_connection.send_game_chat_sync("You're Winner!", [source_player])
            self.discord_connection.send_game_chat_sync("Rebuilding maze")
            self.init_maze()
        pass

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
        if event in self.hooks:
            for trigger_func in self.hooks[event]:
                if inspect.iscoroutine(trigger_func):
                    passed_kwargs = trigger_func.f_kwargs
                    passed_kwargs.update(kwargs)
                    self.aioloop.create_task(trigger_func.func(*trigger_func.f_args, **passed_kwargs))
                else:
                    passed_kwargs = trigger_func.f_kwargs
                    passed_kwargs.update(kwargs)
                    trigger_func.func(*trigger_func.f_args, **passed_kwargs)
                if trigger_func.do_once:
                    self.off(event, trigger_func)


class TriggerFunc:
    def __init__(self, func, do_once=False, *f_args, **f_kwargs):
        self.func = func
        self.f_args = f_args
        self.f_kwargs = f_kwargs
        self.do_once = do_once
