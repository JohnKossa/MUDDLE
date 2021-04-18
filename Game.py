from __future__ import annotations
import asyncio
import inspect
import math
import random

from typing import List, Optional

from game_objects.Character.Character import Character
from game_objects.Enemy import Enemy, Goblin, Kobold, Orc
from game_objects.BossEnemy import StrawGolem, StoneGolem
from game_objects.Maze.Maze import Maze
from game_objects.Town.Town import Town
from game_objects.RoomFixture import TreasureChest
from utils.Scheduler import Scheduler, ScheduledTask
from utils.TriggerFunc import TriggerFunc


class Game:
    from game_objects.Room import Room

    def __init__(self):
        from discord_objects.DiscordUser import DiscordUser
        from DiscordConnection import CustomClient
        self.maze: Maze = None
        self.town: Town = Town()
        self.players_dict: dict = {}
        self.enemies_dict: dict = {}
        self.discord_users: List[DiscordUser] = []
        self.hooks: dict = {}
        self.aioloop = asyncio.get_event_loop()
        self.scheduler: Scheduler = Scheduler(self.aioloop)
        self.discord_connection: Optional[CustomClient] = None

    @property
    def players(self) -> List[Character]:
        return list(self.players_dict.values())

    @property
    def enemies(self) -> List[Enemy]:
        return list(self.enemies_dict.values())

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
                to_add.initialize(self)
                self.discord_connection.send_game_chat_sync(f"Loaded player {to_add.name} for {to_add.discord_user.username}")

    def save_players(self):
        import datetime
        import json
        for player in self.players:
            try:
                player_dict = player.to_dict()
                with open(f"savefiles/characters/{player.name}.json", "w") as outfile:
                    json.dump(player_dict, outfile, indent=4)
            except:
                print(f"Unable to save player {player.name}")
        print("Saving players")
        self.scheduler.schedule_task(
            ScheduledTask(datetime.datetime.now() + datetime.timedelta(minutes=5), self.save_players))

    def setup_hooks(self) -> None:
        import datetime
        self.on("enter_room", TriggerFunc(self.start_combat))
        self.on("player_defeated", TriggerFunc(self.cleanup_dead_player))
        self.on("enemy_defeated", TriggerFunc(self.cleanup_dead_enemy))
        self.on("enemy_defeated", TriggerFunc(self.boss_defeated))
        self.on("maze_reset", TriggerFunc(self.invalidate_player_maps))
        self.scheduler.schedule_task(ScheduledTask(datetime.datetime.now() + datetime.timedelta(minutes=5), self.save_players))

    def invalidate_player_maps(self, **kwargs) -> None:
        for player in self.players:
            maps = list(filter(lambda x: x.name == "DungeonMap", player.inventory.bag))
            for map_item in maps:
                player.inventory.bag.remove(map_item)

    def seed_enemies(self) -> None:
        num_small_enemies = math.isqrt(self.maze.width * self.maze.height)
        viable_rooms = list(filter(lambda x: x != self.maze.entry_room and x != self.maze.exit_room, self.maze.rooms))
        chosen_rooms = random.choices(viable_rooms, k=num_small_enemies)
        for room in chosen_rooms:
            small_enemy_types = [Goblin, Kobold]
            new_enemy = random.choice(small_enemy_types)()
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
        boss_enemy_types = [StrawGolem, StoneGolem]
        boss = random.choice(boss_enemy_types)()
        boss.current_room = self.maze.exit_room
        self.enemies.append(boss)
        self.enemies_dict[boss.guid] = boss

    def seed_loot_stashes(self) -> None:
        viable_rooms = list(filter(lambda x: x != self.maze.entry_room and x != self.maze.exit_room, self.maze.rooms))
        loot_stash_count = math.isqrt(len(viable_rooms))
        viable_rooms.sort(key=lambda x: x.num_neighbors)
        chosen_rooms = viable_rooms[:loot_stash_count]
        for room in chosen_rooms:
            room.fixtures.append(TreasureChest())

    def start_combat(self, source_player: Optional[Character], room: Optional[Room] = None, **kwargs) -> None:
        if room is None:
            return
        if len(room.get_enemies(self)) > 0 and len(room.get_characters(self)) > 0:
            room.start_combat(self)
            return
        if room.combat is not None and not room.combat.processing_round:
            room.combat.add_player(self, source_player)

    def check_final_room(self, room: Optional[Room] = None, source_player: Optional[Character] = None, **kwargs) -> None:
        if room == self.maze.exit_room:
            self.discord_connection.send_game_chat_sync("You're Winner!", [source_player.discord_user])
            self.discord_connection.send_game_chat_sync("Rebuilding maze")
            self.init_maze()
            self.return_players_to_start()

    def boss_defeated(self, source_enemy: Optional[Enemy] = None, room: Optional[Room] = None, **kwargs):
        import datetime
        if room == self.maze.exit_room:
            enemies = room.get_enemies(self)
            enemies = [*filter(lambda x: not x.dead, enemies)]
            if len(enemies) == 0:
                self.discord_connection.send_game_chat_sync("You're Winner!", [x.discord_user for x in room.get_characters(self)])
                self.discord_connection.send_game_chat_sync("With the boss room cleared, the walls begin to dissolve to an inky black smoke. It may not last longer than 10 more minutes.")
                self.scheduler.schedule_task(
                    ScheduledTask(datetime.datetime.now() + datetime.timedelta(minutes=10), self.restart_maze))

    def cleanup_dead_player(self, source_player: Optional[Character] = None, **kwargs):
        source_player.cleanup(self)

    def cleanup_dead_enemy(self, source_enemy: Optional[Enemy] = None, **kwargs):
        source_enemy.cleanup(self)

    def restart_maze(self):
        self.init_maze()
        self.return_players_to_start()
        self.discord_connection.send_game_chat_sync(
            "The labyrinth vanishes into a puff of smoke and re-materializes. You suddenly find yourself in the entrance chamber to a brand new maze.")

    def init_maze(self, width: int = 11, height: int = 11, difficulty: int = 6) -> None:
        if self.maze is not None:
            self.maze.cleanup()
        self.maze = Maze(width=width, height=height)
        self.maze.generate_maze((random.randrange(1, width - 1), width - 1), (random.randrange(1, width - 1), 0), difficulty=difficulty)
        self.delete_all_enemies()
        self.seed_enemies()
        self.seed_loot_stashes()
        self.return_players_to_start()
        if self.discord_connection is not None:
            self.discord_connection.send_game_chat_sync("Rebuilding maze")
        self.trigger("maze_reset", game=self)

    def return_players_to_start(self) -> None:
        for player in self.players:
            player.current_room = self.maze.entry_room

    def delete_all_enemies(self):
        self.enemies_dict = {}

    def register_player(self, new_player: Character) -> None:
        new_player.current_room = self.maze.entry_room
        self.players.append(new_player)
        self.players_dict[new_player.guid] = new_player
        new_player.initialize(self)

    def on(self, event: str, trigger_func: TriggerFunc) -> None:
        if event not in self.hooks:
            self.hooks[event] = []
        self.hooks[event].append(trigger_func)

    def off(self, event: str, trigger_func: TriggerFunc) -> bool:
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
                    passed_kwargs.update({"game": self})
                    self.aioloop.create_task(trigger_func.func(*trigger_func.f_args, **passed_kwargs))
                else:
                    passed_kwargs = trigger_func.f_kwargs
                    passed_kwargs.update(kwargs)
                    passed_kwargs.update({"game": self})
                    trigger_func.func(*trigger_func.f_args, **passed_kwargs)
                if trigger_func.do_once:
                    self.off(event, trigger_func)
