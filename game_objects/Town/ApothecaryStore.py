from __future__ import annotations
from typing import List

from game_objects.Commands.Command import Command
from game_objects.Room import Room


class ApothecaryStore(Room):
    def __init__(self):
        super().__init__(name=f"Apothecary Store")
        self.neighbors: List[Room] = []

    def describe_room(self) -> str:
        # TODO split this into a first visit and subsequent visits description
        return "\n".join([
            "As you step through the door, a pungent smell wafts through the air.",
            "The walls are draped with various herbs hung from bits of twine. Still more are piled high on the shelves behind the counter.",
            "A young girl pokes her head up above the counter. Catching your eye, she slides a wooden crate over and climbs on top of it.",
            """"Welcome to Bottle of Wonders! I'm Hazel. I How can I help you today?" """
        ])

    def get_commands(self, game) -> List[Command]:
        return super().get_commands(game)
