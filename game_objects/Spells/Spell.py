from typing import Any
from game_objects.AttackAction import AttackAction
from game_objects.StatusEffect import StatusEffect
from game_objects.CombatEntity import CombatEntity


class TargetTypes:
    Player = "player"
    Enemy = "enemy"
    Item = "item"


class Spell:
    def __init__(self):
        self.name = ""
        self.mana_cost = 0
        self.actions = 1
        self.usable_in_combat = True
        self.usable_out_of_combat = True
        self.data = {}
        # TODO come up with a way to specify targets declaratively
        self.spell_effect = None
        self.target_type = None
        self.min_targets = 0
        self.max_targets = 1000000
        # TODO possibly do a list of tuples of (target type, min, max)


def attack_effect(targets: list[Any], attack: AttackAction):
    pass


def apply_status_effect(targets: list[Any], status: StatusEffect, chance: float = 1):
    pass


def custom_effect():
    pass
