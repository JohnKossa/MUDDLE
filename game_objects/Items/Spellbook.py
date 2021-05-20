from __future__ import annotations
from typing import List

from game_objects.Commands.Command import Command
from game_objects.Items.Equipment import Equipment


class Spellbook(Equipment):
    def __init__(self):
        super().__init__()
        self.name: str = "Spellbook"
        self.slot: str = "hand"
        self.spells: list = []

    def to_dict(self, full_depth=True) -> dict:
        to_return = super().to_dict() if full_depth else {}
        to_return.update({
            "constructor": self.__class__.__name__,
            "slot": self.slot
        })
        return to_return

    @classmethod
    def from_dict(cls, source_dict) -> Spellbook:
        to_return = Spellbook()
        to_return.__dict__.update(source_dict)
        return to_return

    def get_commands(self, game) -> List[Command]:
        return super().get_commands(game)
