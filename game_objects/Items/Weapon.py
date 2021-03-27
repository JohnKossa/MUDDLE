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

    def to_dict(self, full_depth=True) -> dict:
        to_return = super().to_dict() if full_depth else {}
        to_return.update({
            "constructor": self.__class__.__name__,
            "slot": self.slot,
            "attacks": [attack.to_dict() for attack in self.attacks],
            "default_attack": self.default_attack
        })
        return to_return

    @classmethod
    def from_dict(cls, source_dict) -> Weapon:
        to_return = Weapon()
        to_return.__dict__.update(source_dict)
        to_return.attacks = [AttackAction.from_dict(x) for x in source_dict["attacks"]]
        return to_return

    def get_commands(self) -> List[Command]:
        to_add = []
        for attack in self.attacks:
            if attack.name == self.default_attack:
                to_add.append(AttackCommand(attack, aliases=[attack.name.capitalize(), "Attack", "Atk"]))
            else:
                to_add.append(AttackCommand(attack, aliases=[attack.name.capitalize()]))
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
            AttackAction(name="firepoke", hit_bonus=3, dmg_type="fire", dmg_roll=(1, 6), dmg_bonus=0)
        ]
        self.default_attack: str = "firepoke"


class Dagger(Weapon):
    def __init__(self):
        super().__init__()
        self.name: str = "Dagger"
        self.attacks: List[AttackAction] = [
            AttackAction(name="slash", hit_bonus=1, dmg_type="slash", dmg_roll=(2, 4), dmg_bonus=0),
            AttackAction(name="stab", hit_bonus=3, dmg_type="pierce", dmg_roll=(3, 4), dmg_bonus=0)
        ]
        self.default_attack: str = "stab"


class Mace(Weapon):
    def __init__(self):
        super().__init__()
        self.name: str = "Mace"
        self.attacks: List[AttackAction] = [
            AttackAction(name="strike", hit_bonus=2, dmg_type="bludgeon", dmg_roll=(1, 8), dmg_bonus=1),
            AttackAction(name="spike", hit_bonus=1, dmg_type="pierce", dmg_roll=(1, 6), dmg_bonus=0),
            AttackAction(name="smash", hit_bonus=1, dmg_type="bludgeon", dmg_roll=(1, 16), dmg_bonus=2, action_cost=2)
        ]
        self.default_attack: str = "strike"


class Spear(Weapon):
    def __init__(self):
        super().__init__()
        self.name: str = "Spear"
        self.attacks: List[AttackAction] = [
            AttackAction(name="slash", hit_bonus=1, dmg_type="slash", dmg_roll=(1, 8), dmg_bonus=0),
            AttackAction(name="stab", hit_bonus=2, dmg_type="pierce", dmg_roll=(1, 12), dmg_bonus=2)
        ]
        self.default_attack: str = "stab"


class Axe(Weapon):
    def __init__(self):
        super().__init__()
        self.name: str = "Axe"
        self.attacks: List[AttackAction] = [
            AttackAction(name="slash", hit_bonus=0, dmg_type="slash", dmg_roll=(1, 16), dmg_bonus=0)
        ]
        self.default_attack: str = "slash"
