from __future__ import annotations

from game_objects.Commands.Command import Command
from game_objects.Commands.CombatCommands.BlockCommand import BlockCommand
from game_objects.Items.Equipment import Equipment


class Shield(Equipment):
    def __init__(self):
        super().__init__()
        self.name: str = "IronRoundShield"
        self.traits = self.traits + ["metallic"]
        self.weight = 11
        self._basevalue = 2000
        self.slot: str = "hand"

    def to_dict(self, full_depth=True) -> dict:
        to_return = super().to_dict() if full_depth else {}
        to_return.update({
            "constructor": self.__class__.__name__,
            "slot": self.slot
        })
        return to_return

    @classmethod
    def from_dict(cls, source_dict) -> Shield:
        to_return = Shield()
        to_return.__dict__.update(source_dict)
        return to_return

    def get_commands(self, game) -> list[Command]:
        # will add "block" command
        return super().get_commands(game) + [BlockCommand()]
