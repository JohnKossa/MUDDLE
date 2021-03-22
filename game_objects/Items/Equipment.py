from __future__ import annotations
from typing import Any, List

import Game
from game_objects import Character
from game_objects.Commands.Command import Command
from game_objects.Items.Item import Item


class Equipment(Item):
    def __init__(self):
        super().__init__()
        self.slot: str = ""
        self.max_hitpoints: int = 100
        self.hit_points: int = 100
        self.active_effects: List[Any] = []
        self.resistances: dict = {  # any resistance not specified is assumed to be 0

        }

    def use_effect(self, game: Game, source_player: Character, params: List[Any]):
        # equips the item
        pass

    def get_commands(self) -> List[Command]:
        # will add equip and unequip commands
        return super().get_commands() + []