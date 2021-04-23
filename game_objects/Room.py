from __future__ import annotations
from typing import Any, List, Optional

import Game
from game_objects.Commands.Command import Command
from game_objects.Conversation import Conversation
from game_objects.Commands.PartialCombatCommands.ExitCommand import Exit
from game_objects.Commands.PartialCombatCommands.TakeCommand import Take
from game_objects.Enemy import Enemy
from game_objects.NPC import NPC
from utils.TextHelpers import enumerate_objects, pluralize


class Room:
    from game_objects.Character.Character import Character

    def __init__(self, name: str = ""):
        from game_objects.Combat import Combat
        from game_objects.RoomFixture import Fixture
        from game_objects.Items.Item import Item
        self.name: str = name
        self.aliases: List[str] = []
        self.template: Any = None
        self.fixtures: List[Fixture] = []
        self.items: List[Item] = []
        self.combat: Optional[Combat] = None
        self.conversations: List[Conversation] = []
        self.neighbors: List[Room] = []

    def get_door(self, name: str) -> Optional[Room]:
        # dig through all neighbors by name then alias, returning the correct one
        for neighbor in self.neighbors:
            if neighbor.name.lower() == name.lower():
                return neighbor
        for neighbor in self.neighbors:
            for alias in neighbor.aliases:
                if alias.lower() == name.lower():
                    return neighbor
        for neighbor in self.neighbors:
            no_space_string = neighbor.name.replace(" ", "")
            if no_space_string.lower() == name.lower():
                return neighbor
        for neighbor in self.neighbors:
            for alias in neighbor.aliases:
                no_space_string = alias.replace(" ", "")
                if no_space_string.lower() == name.lower():
                    return neighbor
        for neighbor in self.neighbors:
            underscore_string = neighbor.name.replace(" ", "_")
            if underscore_string.lower() == name.lower():
                return neighbor
        for neighbor in self.neighbors:
            for alias in neighbor.aliases:
                underscore_string = alias.replace(" ", "_")
                if underscore_string.lower() == name.lower():
                    return neighbor
        return None

    def get_characters(self, game: Game) -> List[Character]:
        return list(filter(lambda x: x.current_room == self, game.players))

    def get_enemies(self, game: Game) -> List[Enemy]:
        return list(filter(lambda x: x.current_room == self, game.enemies))

    def get_npcs(self, game: Game) -> List[NPC]:
        return list(filter(lambda x: x.current_room == self, game.npcs))

    def get_commands(self) -> List[Command]:
        from game_objects.Commands.NoncombatCommands.ConversationCommands import TalkCommand, SayCommand
        to_return = [Exit()]
        if len(self.items) > 0:
            to_return.append(Take())
        if len(self.conversations):
            to_return.append(TalkCommand())
            to_return.append(SayCommand())
        for fixture in self.fixtures:
            to_return.extend(fixture.get_commands())
        return to_return

    def start_combat(self, game: Game) -> None:
        from game_objects.Combat import Combat
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

    def describe_entities(self, game: Game):
        enemies = self.get_enemies(game)
        characters = self.get_characters(game)
        npcs = self.get_npcs(game)
        if len(enemies) == 0 and len(npcs) == 0 and len(characters) <= 1:
            return "The room appears to be vacant."
        enemy_counts = {}
        for enemy in enemies:
            if enemy.name not in enemy_counts.keys():
                enemy_counts[enemy.name] = 1
            else:
                enemy_counts[enemy.name] = enemy_counts[enemy.name] + 1
        enemy_count_strings = []
        for name, count in enemy_counts.items():
            enemy_count_strings.append(f"{count} {pluralize(name, count)}")
        for character in characters:
            enemy_count_strings.append(f"{character.name}")
        for npc in npcs:
            enemy_count_strings.append(f"{npc.name}")
        formatted_list = enumerate_objects(enemy_count_strings)
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
        exit_names = [*map(lambda x: x.name, self.neighbors)]
        exit_count = len(exit_names)
        if exit_count == 1:
            return f"There is one exit to the {exit_names[0]}"
        elif exit_count == 2:
            return f"Exits are to the {exit_names[0]} and {exit_names[1]}"
        elif exit_count > 2:
            formatted_list = enumerate_objects(exit_names)
            return f"Exits include {formatted_list}"

    def describe(self, game: Game):
        to_return = self.describe_room()
        entities = self.describe_entities(game)
        fixtures = self.describe_fixtures()
        items = self.describe_items()
        exits = self.describe_exits()
        to_return = to_return + "\n" + entities
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
