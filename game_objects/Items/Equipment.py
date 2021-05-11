from __future__ import annotations
from typing import Any, List

from game_objects.Items.Item import Item


class Equipment(Item):
    from game_objects import Character

    def __init__(self):
        super().__init__()
        self.slot: str = ""
        self.max_hitpoints: int = 100
        self.hit_points: int = 100
        self.active_effects: List[Any] = []
        self.resistances: dict = {  # any resistance not specified is assumed to be 0
        }

    def use_effect(self, game: 'Game', source_player: Character, params: List[Any]):
        # equips the item
        pass

    def get_commands(self, game) -> List['Command']:
        # will add equip and unequip commands
        return super().get_commands(game) + []

    def to_dict(self, full_depth=True) -> dict:
        to_return = super().to_dict() if full_depth else {}
        second_dict = {
            "constructor": self.__class__.__name__,
            "slot": self.slot,
            "max_hitpoints": self.max_hitpoints,
            "hit_points": self.hit_points,
            "active_effects": self.active_effects,
            "resistances": self.resistances
        }
        to_return.update(second_dict)
        return to_return

    @classmethod
    def from_dict(cls, source_dict) -> Equipment:
        to_return = Equipment()
        to_return.__dict__.update(source_dict)
        return to_return
