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

    def to_dict(self, full_depth=True) -> dict:
        to_return = super().to_dict() if full_depth else {}
        to_add = {
            "constructor": self.__class__.__name__,
            "slot": self.slot,
            "damage_resistances": self.damage_resistances,
            "hit_resistances": self.hit_resistances
        }
        to_return.update(to_add)
        return to_return

    @classmethod
    def from_dict(cls, source_dict) -> Armor:
        to_return = Armor()
        to_return.__dict__.update(source_dict)
        return to_return

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


class Gambeson(Armor):
    def __init__(self):
        super().__init__()
        self.name: str = "Gambeson"
        self.damage_resistances: dict = {
            "slash": 1,
            "stab": 0,
            "bludgeon": 2,
            "electricity": 2,
            "ice": 2,
            "fire": -1,
        }
        self.hit_resistances: dict = {
            "slash": 1,
            "stab": 0,
            "bludgeon": 0,
            "electricity": 0,
            "ice": 0,
            "fire": -1
        }

    def get_commands(self) -> List[Command]:
        return super().get_commands() + []
