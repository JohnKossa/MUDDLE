from __future__ import annotations
import asyncio
import inspect
import math
import random

from typing import Callable, List, Optional

from game_objects.Room import Room
from game_objects.RoomFixture import TreasureChest
from game_objects.Character.Character import Character
from game_objects.Enemy import Enemy, Goblin, Orc
from game_objects.Maze.Maze import Maze
from utils.Scheduler import Scheduler, ScheduledTask


class TriggerFunc:
    def __init__(self, func, *f_args, **f_kwargs):
        self.func: Callable = func
        self.f_args = f_args
        self.f_kwargs = f_kwargs
        self.do_once: bool = False


class Game:
    def __init__(self):
        from discord_objects.DiscordUser import DiscordUser
        from DiscordConnection import CustomClient
        self.maze: Maze = None
        self.players_dict: dict = {}
        self.enemies_dict: dict = {}
        self.players: List[Character] = []
        self.enemies: List[Enemy] = []
        self.discord_users: List[DiscordUser] = []
        self.hooks: dict = {}
        self.aioloop = asyncio.get_event_loop()
        self.scheduler: Scheduler = Scheduler(self.aioloop)
        self.discord_connection: Optional[CustomClient] = None

    def load_players(self):
        from os import listdir
        from os.path import isfile, join
        import json
        onlyfiles = [f for f in listdir("savefiles/characters") if isfile(join("savefiles/characters", f))]
        onlyfiles.remove(".gitkeep")
        for file in onlyfiles:
            with open("savefiles/characters/"+file, "r") as infile:
                to_add = Character.from_dict(game=self, source_dict=json.load(infile))
                to_add.current_room = self.maze.entry_room
                to_add.discord_user.current_character = to_add
                self.players_dict[to_add.guid] = to_add
                self.players.append(to_add)
                self.discord_connection.send_game_chat_sync(f"Loaded player {to_add.name} for {to_add.discord_user.username}")

    def save_players(self):
        import datetime
        import json
        for player in self.players:
            with open(f"savefiles/characters/{player.name}.json", "w") as outfile:
                json.dump(player.to_dict(), outfile)
        print("Saving players")
        self.scheduler.schedule_task(
            ScheduledTask(datetime.datetime.now() + datetime.timedelta(minutes=5), self.save_players))

    def setup_hooks(self) -> None:
        import datetime
        self.on("enter_room", TriggerFunc(self.start_combat))
        self.on("enter_room", TriggerFunc(self.check_final_room))
        self.on("player_defeated", TriggerFunc(self.cleanup_dead_player))
        self.on("enemy_defeated", TriggerFunc(self.cleanup_dead_enemy))
        self.scheduler.schedule_task(ScheduledTask(datetime.datetime.now() + datetime.timedelta(minutes=5), self.save_players))
        self.scheduler.schedule_task(ScheduledTask(datetime.datetime.now() + datetime.timedelta(minutes=1), self.check_lists))

    def check_lists(self):
        import datetime
        if set(self.enemies_dict.values()) != set(self.enemies):
            print("Enemies dictionary desynced")
            print(self.enemies_dict.values())
            print(self.enemies)
        if set(self.players_dict.values()) != set(self.players):
            print("Players dictionary desynced")
            print(self.players_dict.values())
            print(self.players)
        self.scheduler.schedule_task(
            ScheduledTask(datetime.datetime.now() + datetime.timedelta(minutes=1), self.check_lists))

    def seed_enemies(self) -> None:
        num_small_enemies = math.isqrt(self.maze.width * self.maze.height)
        viable_rooms = list(filter(lambda x: x != self.maze.entry_room and x != self.maze.exit_room, self.maze.rooms))
        chosen_rooms = random.choices(viable_rooms, k=num_small_enemies)
        for room in chosen_rooms:
            new_enemy = Goblin()
            new_enemy.current_room = room
            self.enemies.append(new_enemy)
            self.enemies_dict[new_enemy.guid] = new_enemy
        num_big_enemies = math.isqrt(num_small_enemies)
        chosen_rooms = random.choices(viable_rooms, k=num_big_enemies)
        for room in chosen_rooms:
            new_enemy = Orc()
            new_enemy.current_room = room
            self.enemies.append(new_enemy)
            self.enemies_dict[new_enemy.guid] = new_enemy

    def seed_loot_stashes(self) -> None:
        viable_rooms = list(filter(lambda x: x != self.maze.entry_room and x != self.maze.exit_room, self.maze.rooms))
        loot_stash_count = math.isqrt(len(viable_rooms))
        viable_rooms.sort(key=lambda x: x.num_neighbors)
        chosen_rooms = viable_rooms[:loot_stash_count]
        for room in chosen_rooms:
            room.fixtures.append(TreasureChest())

    def start_combat(self, room: Optional[Room] = None, **kwargs) -> None:
        if room is None:
            return
        if len(room.get_enemies(self)) > 0 and len(room.get_characters(self)) > 0:
            room.start_combat(self)

    def check_final_room(self, room: Optional[Room] = None, source_player: Optional[Character] = None, **kwargs) -> None:
        if room == self.maze.exit_room:
            self.discord_connection.send_game_chat_sync("You're Winner!", [source_player.discord_user])
            self.discord_connection.send_game_chat_sync("Rebuilding maze")
            self.init_maze()
            self.return_players_to_start()

    def cleanup_dead_player(self, source_player: Optional[Character] = None, **kwargs):
        source_player.cleanup(self)

    def cleanup_dead_enemy(self, source_enemy: Optional[Enemy] = None, **kwargs):
        source_enemy.cleanup(self)

    def init_maze(self, width: int = 11, height: int = 11, difficulty: int = 6) -> None:
        if self.maze is not None:
            self.maze.cleanup()
        self.maze = Maze(width=width, height=height)
        self.maze.generate_maze((random.randrange(1, width - 1), width - 1), (random.randrange(1, width - 1), 0), difficulty=difficulty)
        self.delete_all_enemies()
        self.seed_enemies()
        self.seed_loot_stashes()
        self.return_players_to_start()

    def return_players_to_start(self) -> None:
        for player in self.players:
            player.current_room = self.maze.entry_room

    def delete_all_enemies(self):
        self.enemies = []
        self.enemies_dict = {}

    def register_player(self, new_player: Character) -> None:
        new_player.current_room = self.maze.entry_room
        self.players.append(new_player)
        self.players_dict[new_player.guid] = new_player

    def on(self, event: str, trigger_func: TriggerFunc) -> None:
        if event not in self.hooks:
            self.hooks[event] = []
        self.hooks[event].append(trigger_func)

    def off(self, event, trigger_func) -> bool:
        if event in self.hooks and trigger_func in self.hooks[event]:
            self.hooks[event].remove(trigger_func)
            if len(self.hooks[event]) == 0:
                del self.hooks[event]
            return True
        return False

    def once(self, event, trigger_func) -> None:
        if event not in self.hooks:
            self.hooks[event] = []
        trigger_func.do_once = True
        self.hooks[event].append(trigger_func)

    def trigger(self, event, *args, **kwargs) -> None:
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
