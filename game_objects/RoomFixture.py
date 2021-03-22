from __future__ import annotations
from typing import Any, List

from game_objects.Commands.Command import Command


class Fixture:
    # things you find in rooms like torch sconces, tables
    # they belong to the room and grant additional contextual actions to players in the room
    def __init__(self):
        self.template: Any = None

    def get_commands(self) -> List[Command]:
        return []
