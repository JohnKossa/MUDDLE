from __future__ import annotations
from typing import Dict

from game_objects.AttackAction import AttackAction
from utils.Dice import roll


def calculate_hit(attack: AttackAction, hit_resistances: Dict[str, int]) -> bool:
    matched_hit_resistance = hit_resistances.get(attack.dmg_type, 0)
    hit_roll = roll(1, 20, advantage=attack.hit_bonus)
    miss_roll = roll(1, 20, advantage=matched_hit_resistance)
    if hit_roll <= miss_roll:
        return False
    return True


def calculate_damage(attack: AttackAction, dmg_resistances: Dict[str, int]) -> int:
    matched_dmg_resistance = dmg_resistances.get(attack.dmg_type, 0)
    damage_roll = roll(attack.dmg_roll[0], attack.dmg_roll[1], advantage=(attack.dmg_bonus - matched_dmg_resistance))
    return damage_roll


def sum_resistances(set1: Dict[str, int], set2: Dict[str, int]) -> Dict[str, int]:
    to_return = {}
    known_keys = list(set(set1.keys()) | set(set2.keys()))
    for k in known_keys:
        to_return[k] = set1.get(k, 0) + set2.get(k, 0)
    return to_return


def assign_damage(game, source, target, damage):
    from game_objects.Character.Character import Character
    target.health = max(0, target.health-damage)
    if isinstance(target, Character):
        return f"{target.combat_name} takes {damage} damage. ({target.health} hp left)"
    return f"{target.combat_name} takes {damage} damage."

