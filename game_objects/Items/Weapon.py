from __future__ import annotations
from typing import List

from game_objects.AttackAction import AttackAction
from game_objects.Commands.CombatCommands.AttackCommand import AttackCommand
from game_objects.Commands.Command import Command
from game_objects.Items.Equipment import Equipment


class Weapon(Equipment):
    def __init__(self):
        super().__init__()
        self.slot: str = "hand"
        self.attacks: List[AttackAction] = []
        self.default_attack: str = ""

    @classmethod
    def from_template(cls, template_string) -> Weapon:
        import json
        return Weapon()

    def get_commands(self) -> List[Command]:
        to_add = []
        for attack in self.attacks:
            if attack.name == self.default_attack:
                to_add.append(AttackCommand(attack, aliases=[attack.name, "Attack", "Atk"]))
            else:
                to_add.append(AttackCommand(attack, aliases=[attack.name]))
        return super().get_commands() + to_add


class Sword(Weapon):
    def __init__(self):
        super().__init__()
        self.name: str = "Sword"
        self.attacks: List[AttackAction] = [
            AttackAction(name="slash", hit_bonus=2, dmg_type="slash", dmg_roll=(2, 6), dmg_bonus=1),
            AttackAction(name="stab", hit_bonus=1, dmg_type="pierce", dmg_roll=(1, 12), dmg_bonus=1),
            AttackAction(name="pommelstrike", hit_bonus=0, dmg_type="bludgeon", dmg_roll=(1, 6), dmg_bonus=0)
        ]
        self.default_attack: str = "slash"

    def get_commands(self) -> List[Command]:
        return super().get_commands() + []


class Torch(Weapon):
    def __init__(self):
        super().__init__()
        self.name: str = "Torch"
        self.attacks: List[AttackAction] = [
            AttackAction(name="firepoke", hit_bonus=3, dmg_type="fire", dmg_roll=(1,6), dmg_bonus=0)
        ]
        self.default_attack: str = "firepoke"
