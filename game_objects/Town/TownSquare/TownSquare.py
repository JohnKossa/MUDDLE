from __future__ import annotations

from game_objects.Commands.Command import Command
from game_objects.Commands.NoncombatCommands.EnterMazeCommand import EnterMazeCommand
from game_objects.Room import Room
from game_objects.Town.TownSquare.Fixtures.DonationBox import DonationBox
from game_objects.Town.TownSquare.Fixtures.WishingWell import WishingWell


class TownSquare(Room):
    def __init__(self):
        super().__init__(name=f"Town Square")
        self.neighbors: list[Room] = []
        self.fixtures.append(DonationBox())
        self.fixtures.append(WishingWell())

    def describe_room(self) -> str:
        return "You are in the town square. It's super interesting."

    def get_commands(self, game) -> list[Command]:
        to_return = super().get_commands(game)
        return to_return + [EnterMazeCommand()]
