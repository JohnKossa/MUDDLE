from __future__ import annotations
from typing import List

from game_objects.Commands.Command import Command
from game_objects.Commands.CombatCommands.BlockCommand import BlockCommand
from game_objects.Items.Equipment import Equipment


class Shield(Equipment):
    def __init__(self):
        super().__init__()
        self.name: str = "IronRoundShield"
        self.slot: str = "hand"

    @classmethod
    def from_template(cls, template_string) -> Shield:
        import json
        return Shield()

    def get_commands(self) -> List[Command]:
        # will add "block" command
        return super().get_commands() + [BlockCommand()]