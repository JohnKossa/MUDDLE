from __future__ import annotations
from typing import Optional, List

import Game
import utils.TriggerFunc


class CharacterSkills:
    from game_objects.Commands.Command import Command
    from game_objects.Character.Character import Character

    def __init__(self, source_character: Character):
        self.current_character = source_character
        cartography = CartographySkill(self.current_character)
        cartography.level = 1
        self.skill_entries = {"Cartography": cartography}

    def get_by_name(self, name: str) -> CharacterSkill:
        return next(filter(lambda x: x.name == name, self.skill_entries.values()), None)

    def setup_triggers(self, game: Game) -> None:
        for skill in self.skill_entries.values():
            skill.setup_triggers(game)

    def add_proficiency(self, skill_name, amount):
        pass

    def to_dict(self) -> dict:
        return {}

    @classmethod
    def from_dict(cls, source_dict, character):
        return CharacterSkills(character)

    def get_commands(self, game) -> List[Command]:
        return []


class CharacterSkill(object):
    def __init__(self, source_character):
        self.current_character = source_character
        self.name: str = ""
        self.level: int = 0
        self.proficiency: int = 0
        self.proficiency_milestones = {}
        self.data = {}

    def add_proficiency(self, amount):
        pass

    def setup_triggers(self, game: Game) -> None:
        pass

    def get_commands(self):
        pass


class CartographySkill(CharacterSkill):
    from game_objects.Room import Room
    from game_objects.Character.Character import Character

    def __init__(self, source_character):
        super().__init__(source_character)
        self.name = "Cartography"

    def setup_triggers(self, game: Game) -> None:
        # TODO on maze reset, clear visited rooms
        game.on("maze_reset", utils.TriggerFunc.TriggerFunc(self.clear_visited_rooms))
        if self.level >= 1:
            game.on("enter_room", utils.TriggerFunc.TriggerFunc(self.add_to_map))

    def clear_visited_rooms(self, **kwargs) -> None:
        self.data["visited_rooms"] = []

    def add_to_map(self, source_player: Character, room: Optional[Room] = None, **kwargs) -> None:
        if source_player != self.current_character:
            return
        if "visited_rooms" in self.data.keys():
            self.data["visited_rooms"].append(room)
        else:
            self.data["visited_rooms"] = [room]
        self.proficiency = self.proficiency + 1


class CombatSense(CharacterSkill):
    def __init__(self, source_character):
        super().__init__(source_character)
        self.name = "CombatSense"

    def get_commands(self):
        # add the !sizeup command
        pass


class DungeonLore(CharacterSkill):
    def __init__(self, source_character):
        super().__init__(source_character)
        self.name = "DungeonLore"

    def get_commands(self):
        # add the !lookup command
        pass
