from __future__ import annotations
from typing import List, Optional

from game_objects.Commands.Command import Command
from game_objects.Commands.NoncombatCommands.EnterMazeCommand import EnterMazeCommand
from game_objects.Room import Room


class TownSquare(Room):
    def __init__(self):
        super().__init__(name=f"Town Square")
        self.neighbors: List[Room] = []

    def describe_room(self) -> str:
        return "You are in the town square. It's super interesting."

    def get_commands(self) -> List[Command]:
        to_return = super().get_commands()
        return to_return + [EnterMazeCommand()]
