from __future__ import annotations
from typing import Optional, List

import Game


class CharacterSkills:
    from game_objects.Commands.Command import Command

    def __init__(self):
        cartography = CartographySkill()
        cartography.level = 1
        self.skill_entries = {"Cartography": cartography}

    def get_by_name(self, name: str) -> CharacterSkill:
        return next(filter(lambda x: x.name == name, self.skill_entries.values()), None)

    def setup_triggers(self, game: Game) -> None:
        for skill in self.skill_entries.values():
            skill.setup_triggers(game)

    def add_proficiency(self, skill_name, amount):
        pass

    def to_dict(self):
        return {}

    @classmethod
    def from_dict(cls, source_dict):
        return CharacterSkills()

    def get_commands(self) -> List[Command]:
        return []


class CharacterSkill(object):
    def __init__(self):
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

    def __init__(self):
        super().__init__()
        self.name = "Cartography"

    def setup_triggers(self, game: Game) -> None:
        if self.level >= 1:
            game.on("enter_room", Game.TriggerFunc(self.add_to_map))

    def add_to_map(self, room: Optional[Room] = None, **kwargs) -> None:
        print("room visit added to map")
        if "visited_rooms" in self.data.keys():
            self.data["visited_rooms"].append(room)
        else:
            self.data["visited_rooms"] = [room]
        self.proficiency = self.proficiency + 1


class CombatSense(CharacterSkill):
    def __init__(self):
        super().__init__()
        self.name = "CombatSense"

    def get_commands(self):
        # add the !sizeup command
        pass


class DungeonLore(CharacterSkill):
    def __init__(self):
        super().__init__()
        self.name = "DungeonLore"

    def get_commands(self):
        # add the !lookup command
        pass
