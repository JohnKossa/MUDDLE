from __future__ import annotations

from game_objects.Commands.Command import Command
from game_objects.RoomFixture import Fixture


class WishingWell(Fixture):
    def __init__(self):
        super().__init__()
        self.name = "Wishing Well"
        self.aliases = ["Well"]

    def describe(self) -> str:
        return "In the center of the town square sits a simple stone well. It's old; incalculably old. There's no telling how long it's been here. It's not very interesting."

    def get_commands(self, game) -> list[Command]:
        # TODO will add a donate command
        return super().get_commands(game)