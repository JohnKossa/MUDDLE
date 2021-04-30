from __future__ import annotations
from typing import Any, List

from game_objects.Commands.Command import Command
from game_objects.RoomFixture import Fixture


class DonationBox(Fixture):
    def __init__(self):
        super().__init__()
        self.name = "Donation Box"
        self.aliases = ["Box"]

    def describe(self) -> str:
        return "Off to the side is a simple wooden box on a post. It's heavily weathered."

    def get_commands(self, game) -> List[Command]:
        # TODO will add a donate command
        return super().get_commands(game)
