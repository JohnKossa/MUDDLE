from __future__ import annotations

from game_objects.Items.Equipment import Equipment
from utils.Constanats import DamageTypes


class Weapon(Equipment):
    from game_objects.Commands.Command import Command

    def __init__(self, **kwargs):
        from game_objects.AttackAction import AttackAction
        super().__init__(**kwargs)
        self.slot: str = "hand"
        self.attacks: list[AttackAction] = []
        self.default_attack: str = ""
        self.crit_behavior = "default"

    def to_dict(self, full_depth=True) -> dict:
        to_return = super().to_dict() if full_depth else {}
        to_return.update({
            "constructor": self.__class__.__name__,
            "slot": self.slot,
            "attacks": [attack.to_dict() for attack in self.attacks],
            "default_attack": self.default_attack,
            "crit_behavior": self.crit_behavior
        })
        return to_return

    @classmethod
    def from_dict(cls, source_dict) -> Weapon:
        from game_objects.AttackAction import AttackAction
        to_return = Weapon()
        to_return.__dict__.update(source_dict)
        to_return.attacks = [AttackAction.from_dict(x) for x in source_dict["attacks"]]
        return to_return

    def get_commands(self, game) -> list[Command]:
        from game_objects.Commands.CombatCommands.AttackCommand import AttackCommand
        to_add = []
        for attack in self.attacks:
            if attack.name == self.default_attack:
                to_add.append(AttackCommand(attack, aliases=[attack.name.capitalize(), "Attack", "Atk"], weapon=self))
            else:
                to_add.append(AttackCommand(attack, aliases=[attack.name.capitalize()]))
        return super().get_commands(game) + to_add


class Sword(Weapon):
    from game_objects.Commands.Command import Command

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from game_objects.AttackAction import AttackAction
        self.name: str = "Sword"
        self.weight = 6.6
        self._basevalue = 1500
        self.traits = self.traits + ["metallic"]
        self.attacks: list[AttackAction] = [
            AttackAction(name="slash", hit_bonus=2, dmg_type=DamageTypes.Slash, dmg_roll=(2, 6), dmg_bonus=1),
            AttackAction(name="stab", hit_bonus=1, dmg_type=DamageTypes.Pierce, dmg_roll=(1, 12), dmg_bonus=1),
            AttackAction(name="pommelstrike", hit_bonus=0, dmg_type=DamageTypes.Bludgeon, dmg_roll=(1, 6), dmg_bonus=0)
        ]
        self.default_attack: str = "slash"

    def get_commands(self, game) -> list[Command]:
        return super().get_commands(game) + []


class Torch(Weapon):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from game_objects.AttackAction import AttackAction
        self.name: str = "Torch"
        self.traits = self.traits + ["elemental_weapon", "light_source", "simple_weapon"]
        self._basevalue = 1
        self.weight = 2.2
        self.max_stack_size = 5
        self.attacks: list[AttackAction] = [
            AttackAction(name="firepoke", hit_bonus=3, dmg_type=DamageTypes.Fire, dmg_roll=(1, 12), dmg_bonus=-1)
        ]
        self.default_attack: str = "firepoke"
        self.crit_behavior: str = "apply_status_fire"


class Dagger(Weapon):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from game_objects.AttackAction import AttackAction
        self.name: str = "Dagger"
        self.traits = self.traits + ["metallic", "simple_weapon"]
        self._basevalue = 200
        self.weight = 2.2
        self.max_stack_size = 10
        self.attacks: list[AttackAction] = [
            AttackAction(name="slash", hit_bonus=1, dmg_type=DamageTypes.Slash, dmg_roll=(2, 4), dmg_bonus=0),
            AttackAction(name="stab", hit_bonus=3, dmg_type=DamageTypes.Pierce, dmg_roll=(3, 4), dmg_bonus=0)
        ]
        self.default_attack: str = "stab"


class DuelistDagger(Weapon):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from game_objects.AttackAction import AttackAction
        self.name: str = "DuelistDagger"
        self.traits = self.traits + ["metallic"]
        self.weight = 2.2
        self._basevalue = 2000
        self.attacks: list[AttackAction] = [
            AttackAction(name="slash", hit_bonus=1, dmg_type=DamageTypes.Slash, dmg_roll=(2, 4), dmg_bonus=0),
            AttackAction(name="stab", hit_bonus=3, dmg_type=DamageTypes.Pierce, dmg_roll=(3, 4), dmg_bonus=0)
        ]
        self.default_attack: str = "stab"
        self.crit_behavior = "triple_dmg"


class WerebatFang(Weapon):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from game_objects.AttackAction import AttackAction
        self.name: str = "WerebatFang"
        self.weight = 2.2
        self._basevalue = 2000
        self.attacks: list[AttackAction] = [
            AttackAction(name="impale", hit_bonus=3, dmg_type=DamageTypes.Pierce, dmg_roll=(3, 4), dmg_bonus=0)
        ]
        self.default_attack: str = "impale"
        self.crit_behavior = "vampirism"


class Mace(Weapon):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from game_objects.AttackAction import AttackAction
        self.name: str = "Mace"
        self.traits = self.traits + ["metallic"]
        self.weight = 8.8
        self._basevalue = 1200
        self.attacks: list[AttackAction] = [
            AttackAction(name="strike", hit_bonus=2, dmg_type=DamageTypes.Bludgeon, dmg_roll=(1, 8), dmg_bonus=1),
            AttackAction(name="spike", hit_bonus=1, dmg_type=DamageTypes.Pierce, dmg_roll=(1, 6), dmg_bonus=0),
            AttackAction(name="smash", hit_bonus=1, dmg_type=DamageTypes.Bludgeon, dmg_roll=(1, 16), dmg_bonus=2, action_cost=2)
        ]
        self.default_attack: str = "strike"


class CrudgelOfChione(Weapon):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from game_objects.AttackAction import AttackAction
        self.name: str = "CrudgelOfChione"
        self.weight = 8.8
        self._basevalue = 12000
        self.attacks: list[AttackAction] = [
            AttackAction(name="froststrike", hit_bonus=2, dmg_type=DamageTypes.Ice, dmg_roll=(1, 8), dmg_bonus=1),
            AttackAction(name="strike", hit_bonus=2, dmg_type=DamageTypes.Bludgeon, dmg_roll=(1, 8), dmg_bonus=1),
            AttackAction(name="smash", hit_bonus=1, dmg_type=DamageTypes.Bludgeon, dmg_roll=(1, 16), dmg_bonus=2, action_cost=2)
        ]
        self.default_attack: str = "froststrike"
        self.crit_behavior = "apply_status_chilled"


class Spear(Weapon):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from game_objects.AttackAction import AttackAction
        self.name: str = "Spear"
        self.traits = self.traits + ["metallic"]
        self.weight = 6.6
        self._basevalue = 200
        self.attacks: list[AttackAction] = [
            AttackAction(name="slash", hit_bonus=1, dmg_type=DamageTypes.Slash, dmg_roll=(1, 8), dmg_bonus=0),
            AttackAction(name="stab", hit_bonus=2, dmg_type=DamageTypes.Pierce, dmg_roll=(1, 12), dmg_bonus=2)
        ]
        self.default_attack: str = "stab"


class PerunsPike(Weapon):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from game_objects.AttackAction import AttackAction
        self.name: str = "PerunsPike"
        self.traits = self.traits + ["metallic"]
        self.weight = 39.6
        self._basevalue = 2000
        self.attacks: list[AttackAction] = [
            AttackAction(name="shock", hit_bonus=1, dmg_type=DamageTypes.Electricity, dmg_roll=(1, 12), dmg_bonus=2),
            AttackAction(name="stab", hit_bonus=2, dmg_type=DamageTypes.Pierce, dmg_roll=(1, 12), dmg_bonus=1)
        ]
        self.default_attack: str = "shock"


class Axe(Weapon):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from game_objects.AttackAction import AttackAction
        self.name: str = "Axe"
        self.traits = self.traits + ["metallic"]
        self.weight = 8.8
        self._basevalue = 2000
        self.attacks: list[AttackAction] = [
            AttackAction(name="slash", hit_bonus=0, dmg_type=DamageTypes.Slash, dmg_roll=(1, 16), dmg_bonus=0)
        ]
        self.default_attack: str = "slash"


class RavensBeak(Weapon):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from game_objects.AttackAction import AttackAction
        self.name: str = "RavensBeak"
        self.weight = 13.2
        self._basevalue = 1500
        self.traits = self.traits + ["metallic"]
        self.attacks: list[AttackAction] = [
            AttackAction(name="stab", hit_bonus=2, dmg_type=DamageTypes.Pierce, dmg_roll=(1, 12), dmg_bonus=0),
            AttackAction(name="spike", hit_bonus=1, dmg_type=DamageTypes.Pierce, dmg_roll=(1, 16), dmg_bonus=2, action_cost=2),
            AttackAction(name="hammer", hit_bonus=1, dmg_type=DamageTypes.Bludgeon, dmg_roll=(1, 16), dmg_bonus=2, action_cost=2),
        ]
        self.default_attack: str = "stab"
