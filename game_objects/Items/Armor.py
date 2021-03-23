from __future__ import annotations
from typing import List

from game_objects.Commands.Command import Command
from game_objects.Items.Equipment import Equipment


class Armor(Equipment):
    def __init__(self):
        super().__init__()
        self.slot: str = "Body"
        # resistances bestowed to user when equipped. assumed to be 0 if not specified
        self.damage_resistances: dict = {}
        self.hit_resistances: dict = {}

    @classmethod
    def from_template(cls, template_string) -> Armor:
        import json
        return Armor()

    def get_commands(self) -> List[Command]:
        return super().get_commands() + []


class PlateArmor(Armor):
    def __init__(self):
        super().__init__()
        # resistances bestowed to user when equipped. assumed to be 0 if not specified
        self.name: str = "IronPlate"
        self.damage_resistances: dict = {
            "slash": 2,
            "stab": 0,
            "bludgeon": 1,
            "electricity": -5
        }
        self.hit_resistances: dict = {
            "slash": 2,
            "stab": 1,
            "bludgeon": 0,
            "electricity": -1
        }

    def get_commands(self) -> List[Command]:
        return super().get_commands() + []


class ChainArmor(Armor):
    def __init__(self):
        super().__init__()
        # resistances bestowed to user when equipped. assumed to be 0 if not specified
        self.name: str = "IronChainmail"
        self.damage_resistances: dict = {
            "slash": 2,
            "stab": 1,
            "bludgeon": 1,
            "electricity": -3
        }
        self.hit_resistances: dict = {
            "slash": 2,
            "stab": 1,
            "bludgeon": 0,
            "electricity": -1
        }

    def get_commands(self) -> List[Command]:
        return super().get_commands() + []
