from __future__ import annotations
import random
from typing import List, Optional

import Game
from game_objects.Commands.Command import Command
from game_objects.Room import Room


class MageShop(Room):
    def __init__(self):
        super().__init__(name=f"Mage Shop")
        self.neighbors: List[Room] = []

    def describe_room(self) -> str:
        return "You are at the Mage Shop. It's super interesting."

    def get_commands(self, game) -> List[Command]:
        return super().get_commands(game)
