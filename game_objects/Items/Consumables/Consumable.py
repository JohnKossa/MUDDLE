from __future__ import annotations
from typing import Any, List
import Game
from game_objects.Character.Character import Character
from game_objects.Items.Item import Item


class Consumable(Item):
    def __init__(self):
        super().__init__()

    def use_effect(self, game: Game, source_player: Character, params: List[Any]) -> None:
        # describes what happens when a player does !use with the item
        raise Exception(f"use_effect not implemented for {self.name}")
