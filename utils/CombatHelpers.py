from __future__ import annotations
from typing import Callable, Dict, Optional

from game_objects.AttackAction import AttackAction

from utils.Dice import roll


def calculate_hit(attack: AttackAction, player_hit_bonus, hit_resistances: Dict[str, int]) -> str:
    matched_hit_resistance = hit_resistances.get(attack.dmg_type, 0)
    hit_roll = roll(1, 20, advantage=attack.hit_bonus+player_hit_bonus)
    miss_roll = roll(1, 20, advantage=matched_hit_resistance)
    # print(f"Rolled {hit_roll} vs {miss_roll} diff is {hit_roll-miss_roll}")
    if hit_roll <= miss_roll:
        return "miss"
    if (hit_roll - miss_roll) > 10:
        return "critical"
    return "hit"


def calculate_damage(attack: AttackAction, player_dmg_bonus, dmg_resistances: Dict[str, int]) -> int:
    matched_dmg_resistance = dmg_resistances.get(attack.dmg_type, 0)
    damage_roll = roll(attack.dmg_roll[0], attack.dmg_roll[1], advantage=(attack.dmg_bonus + player_dmg_bonus - matched_dmg_resistance))
    return damage_roll


def sum_resistances(set1: Dict[str, int], set2: Dict[str, int]) -> Dict[str, int]:
    to_return = {}
    known_keys = list(set(set1.keys()) | set(set2.keys()))
    for k in known_keys:
        to_return[k] = set1.get(k, 0) + set2.get(k, 0)
    return to_return


def assign_damage(game, source, target, damage) -> str:
    from game_objects.Character.Character import Character
    target.health = max(0, target.health-damage)
    if isinstance(target, Character):
        return f"{target.combat_name} takes {damage} damage. ({target.display_health} hp left)"
    return f"{target.combat_name} takes {damage} damage."


class CritBehaviors:
    import Game
    from game_objects.AttackAction import AttackAction
    from game_objects.CombatEntity import CombatEntity
    from game_objects.Items.Weapon import Weapon

    @staticmethod
    def get_by_name(name) -> Callable:
        mappings = {
            "default": CritBehaviors.double_damage,
            "apply_status_fire": CritBehaviors.apply_status_fire,
            "double_dmg": CritBehaviors.double_damage,
            "triple_dmg": CritBehaviors.triple_damage,
            "vampirism": CritBehaviors.vampirism
        }
        return mappings.get(name, CritBehaviors.double_damage)

    @staticmethod
    def double_damage(game: Game, attack_action: AttackAction, source: CombatEntity, target: CombatEntity, weapon: Optional[Weapon], **kwargs):
        """Roll damage twice"""
        from utils.Constanats import Triggers
        dmg_bonus = target.dmg_bonus
        dmg_resistance = target.resistances["dmg"]
        damage_to_assign = calculate_damage(attack_action, dmg_bonus, dmg_resistance) + calculate_damage(
            attack_action, dmg_bonus, dmg_resistance)
        assign_damage_response = target.assign_damage(game, source, target, damage_to_assign)
        game.discord_connection.send_game_chat_sync(
            f"{source.combat_name} uses {attack_action.name}. Critical hit! " + assign_damage_response)
        game.trigger(Triggers.AttackHit, source=source, target=target, damage=damage_to_assign)

    @staticmethod
    def triple_damage(game: Game, attack_action: AttackAction, source: CombatEntity, target: CombatEntity, weapon: Optional[Weapon], **kwargs):
        """Roll damage three times"""
        from utils.Constanats import Triggers
        dmg_bonus = target.dmg_bonus
        dmg_resistance = target.resistances["dmg"]
        damage_to_assign = calculate_damage(attack_action, dmg_bonus, dmg_resistance) + calculate_damage(
            attack_action, dmg_bonus, dmg_resistance) + calculate_damage(
            attack_action, dmg_bonus, dmg_resistance)
        assign_damage_response = target.assign_damage(game, source, target, damage_to_assign)
        game.discord_connection.send_game_chat_sync(
            f"{source.combat_name} uses {attack_action.name}. Critical hit! " + assign_damage_response)
        game.trigger(Triggers.AttackHit, source=source, target=target, damage=damage_to_assign)

    @staticmethod
    def apply_status_fire(game: Game, attack_action: AttackAction, source: CombatEntity, target: CombatEntity, weapon: Optional[Weapon], **kwargs):
        """Apply onfire status to target"""
        from game_objects.Statuses.OnFireStatus import OnFireStatus
        from utils.Constanats import Triggers
        dmg_bonus = target.dmg_bonus
        dmg_resistance = target.resistances["dmg"]
        damage_to_assign = calculate_damage(attack_action, dmg_bonus, dmg_resistance)
        assign_damage_response = target.assign_damage(game, source, target, damage_to_assign)
        fire_status = OnFireStatus(target)
        target.add_status(game, fire_status)
        game.discord_connection.send_game_chat_sync(
            f"{source.combat_name} uses {attack_action.name}. Critical hit! " + assign_damage_response)
        game.discord_connection.send_game_chat_sync(f"{target.combat_name} is engulfed in flames!")
        game.trigger(Triggers.AttackHit, source=source, target=target, damage=damage_to_assign)

    @staticmethod
    def vampirism(game: Game, attack_action: AttackAction, source: CombatEntity, target: CombatEntity, weapon: Optional[Weapon], **kwargs):
        """Roll damage and restore that amount of health in addition to the damage"""
        from utils.Constanats import Triggers
        dmg_bonus = target.dmg_bonus
        dmg_resistance = target.resistances["dmg"]
        damage_to_assign = calculate_damage(attack_action, dmg_bonus, dmg_resistance)
        assign_damage_response = target.assign_damage(game, source, target, damage_to_assign)
        damage_to_restore = min(damage_to_assign, source.max_health-source.health)
        source.health = source.health + damage_to_restore
        game.discord_connection.send_game_chat_sync(
            f"{source.combat_name} uses {attack_action.name}. Critical hit! " + assign_damage_response + f" {source.combat_name} restores {damage_to_assign} health.")
        game.trigger(Triggers.AttackHit, source=source, target=target, damage=damage_to_assign)

