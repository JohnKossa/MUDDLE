from __future__ import annotations
from typing import Any, List, Optional

import Game
from game_objects.Character import Character
from game_objects.Combat import Combat
from game_objects.Commands.Command import Command
from game_objects.Commands.PartialCombatCommands.TakeCommand import Take
from game_objects.Enemy import Enemy
from utils.TextHelpers import enumerate_objects, pluralize


class Room:
    def __init__(self, name: str = ""):
        from game_objects.RoomFixture import Fixture
        from game_objects.Items.Item import Item
        self.name: str = name
        self.template: Any = None
        self.fixtures: List[Fixture] = []
        self.items: List[Item] = []
        self.combat: Optional[Combat] = None

    def get_characters(self, game: Game) -> List[Character]:
        return list(filter(lambda x: x.current_room == self, game.players))

    def get_enemies(self, game: Game) -> List[Enemy]:
        return list(filter(lambda x: x.current_room == self, game.enemies))

    def get_commands(self) -> List[Command]:
        to_return = []
        if len(self.items) > 0:
            to_return.append(Take())
        for fixture in self.fixtures:
            to_return.extend(fixture.get_commands())
        return to_return

    def start_combat(self, game: Game) -> None:
        if self.combat is not None:
            return
        self.combat = Combat(players=self.get_characters(game), enemies=self.get_enemies(game), room=self)
        self.combat.start(game)

    def end_combat(self) -> None:
        del self.combat
        self.combat = None

    def describe_room(self) -> str:
        # TODO link this to the correct room template file and pull the description from there
        if self.template is None:
            return f"You are in a room. It's super interesting. {self.name}"
        return self.template

    def describe_enemies(self, game: Game):
        enemies = self.get_enemies(game)
        if len(enemies) == 0:
            return "The room appears to be vacant."
        enemy_counts = {}
        for enemy in enemies:
            if enemy.name not in enemy_counts.keys():
                enemy_counts[enemy.name] = 1
            else:
                enemy_counts[enemy.name] = enemy_counts[enemy.name] + 1
        count_strings = []
        for name, count in enemy_counts.items():
            count_strings.append(f"{count} {pluralize(name, count)}")
        formatted_list = enumerate_objects(count_strings)
        return f"In the room, you see {formatted_list}"

    def describe_fixtures(self) -> Optional[str]:
        if len(self.fixtures) == 0:
            return None
        return "\n".join([x.describe() for x in self.fixtures])

    def describe_items(self) -> Optional[str]:
        if self.items is None or len(self.items) == 0:
            return None
        item_count = len(self.items)
        if item_count == 1:
            return f"On the floor you see {self.items[0].describe()}."
        if item_count == 2:
            return f"On the floor you see {self.items[0].describe()} and {self.items[1].describe()}"
        else:
            formatted_list = enumerate_objects(list(map(lambda x: x.describe(), self.items)))
            return f"A large assortment of items is strewn about the floor including {formatted_list}"

    def describe_exits(self) -> str:
        return ""

    def describe(self, game: Game):
        to_return = self.describe_room()
        enemies = self.describe_enemies(game)
        fixtures = self.describe_fixtures()
        items = self.describe_items()
        exits = self.describe_exits()
        to_return = to_return + "\n" + enemies
        if fixtures is not None:
            to_return = to_return + "\n" + fixtures
        if items is not None:
            to_return = to_return + "\n" + items
        to_return = to_return + "\n" + exits
        return to_return

    def __str__(self):
        to_return = self.describe_room()
        fixtures = self.describe_fixtures()
        items = self.describe_items()
        exits = self.describe_exits()
        if fixtures is not None:
            to_return = to_return+"\n"+fixtures
        if items is not None:
            to_return = to_return+"\n"+items
        to_return = to_return+"\n"+exits
        return to_return
