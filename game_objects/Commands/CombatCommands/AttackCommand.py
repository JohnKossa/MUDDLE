from __future__ import annotations

import random
from typing import Any, Optional

import Game

from game_objects.Commands.CombatCommands.CombatCommand import CombatOnlyCommand
from utils.CombatHelpers import calculate_hit, calculate_damage


class AttackCommand(CombatOnlyCommand):
    from game_objects.CombatEntity import CombatEntity
    from game_objects.AttackAction import AttackAction
    from game_objects.Items.Weapon import Weapon

    def __init__(self, attack_action: AttackAction, aliases: list[str] = None, weapon: Optional[Weapon] = None):
        from game_objects.AttackAction import AttackAction
        super().__init__()
        self.combat_action_cost: int = attack_action.action_cost
        self.source_weapon = weapon
        self.attack_action: AttackAction = attack_action
        if aliases is not None:
            self.aliases: list[str] = aliases
        else:
            self.aliases: list[str] = [
                "Attack",
                "Atk"
            ]

    @classmethod
    def show_help(cls) -> str:
        # TODO Correct this
        return "\n".join([
            "Performs the default attack for the weapon against the specified target.",
            "If no target is specified, the attack will target the first valid enemy",
            "Params:",
            "   0: Name of the enemy to attack (optional)"
        ])

    def command_valid(self, game: Game, source_player: CombatEntity, params: list[Any]) -> bool:
        from game_objects.Character.Character import Character
        from game_objects.Enemy import Enemy
        from utils.CommandHelpers import match_enemy, match_player
        enemies = source_player.current_room.combat.enemies
        players = source_player.current_room.combat.players
        target = None
        if len(params) > 0:
            match_enemy_result = match_enemy(enemies, params)
            if match_enemy_result is not None:
                target = match_enemy_result
            else:
                match_player_result = match_player(players, params)
                if match_player_result is not None:
                    target = match_player_result
        elif isinstance(source_player, Character):
            if len(enemies) == 0:
                return False
            target = random.choice(enemies)
        elif isinstance(source_player, Enemy):
            if len(players) == 0:
                return False
            target = random.choice(players)
        if target is None:
            return False
        return True

    def do_combat_action(self, game: Game, source_player: CombatEntity, params: list[Any]) -> None:
        from game_objects.Character.Character import Character
        from game_objects.Enemy import Enemy
        from utils.CommandHelpers import match_enemy, match_player
        from utils.CombatHelpers import CritBehaviors
        from utils.Constanats import Triggers
        enemies = source_player.current_room.combat.enemies
        players = source_player.current_room.combat.players
        target = None
        if len(params):
            match_enemy_result = match_enemy(enemies, params)
            if match_enemy_result is not None:
                target = match_enemy_result
            else:
                match_player_result = match_player(players, params)
                if match_player_result is not None:
                    target = match_player_result
        elif isinstance(source_player, Character):
            if len(enemies) == 0:
                return
            target = random.choice(enemies)
        elif isinstance(source_player, Enemy):
            if len(players) == 0:
                return
            target = random.choice(players)
        if target is None:
            return
        hit_bonus = source_player.hit_bonus
        dmg_bonus = target.dmg_bonus
        hit_resistance = target.resistances["hit"]
        dmg_resistance = target.resistances["dmg"]
        hit_result = calculate_hit(self.attack_action, hit_bonus, hit_resistance)
        if hit_result == "miss":
            game.discord_connection.send_game_chat_sync(
                f"{source_player.combat_name} uses {self.attack_action.name}. It misses.")
            return
        elif hit_result == "critical":
            crit_func_name = "default" if self.source_weapon is None else self.source_weapon.crit_behavior
            CritBehaviors.get_by_name(crit_func_name)(game, self.attack_action, source_player, target, self.source_weapon)
        else:
            damage_to_assign = calculate_damage(self.attack_action, dmg_bonus, dmg_resistance)
            assign_damage_response = target.assign_damage(game, source_player, target, damage_to_assign)
            game.discord_connection.send_game_chat_sync(f"{source_player.combat_name} uses {self.attack_action.name}. "+assign_damage_response)
            game.trigger(Triggers.AttackHit, source=source_player, target=target, damage=damage_to_assign)
