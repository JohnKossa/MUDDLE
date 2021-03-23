from __future__ import annotations

import random
from typing import Any, List

import Game

from game_objects.CombatEntity import CombatEntity
from game_objects.Commands.CombatCommands.CombatCommand import CombatOnlyCommand
from utils.CombatHelpers import calculate_hit, calculate_damage


class AttackCommand(CombatOnlyCommand):
    from game_objects.AttackAction import AttackAction

    def __init__(self, attack_action: AttackAction, aliases: List[str] = None):
        from game_objects.AttackAction import AttackAction
        super().__init__()
        self.combat_action_cost: int = attack_action.action_cost
        self.attack_action: AttackAction = attack_action
        if aliases is not None:
            self.aliases: List[str] = aliases
        else:
            self.aliases: List[str] = [
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

    def do_combat_action(self, game: Game, source_player: CombatEntity, params: List[Any]) -> None:
        from game_objects.Character import Character
        from game_objects.Enemy import Enemy
        enemies = source_player.current_room.combat.enemies
        players = source_player.current_room.combat.players
        target = None
        if len(params):
            for enemy in enemies:
                if enemy.combat_name == params[0]:
                    target = enemy
            for player in players:
                if player.combat_name == params[0]:
                    target = player
        elif isinstance(source_player, Character):
            if len(enemies) == 0:
                return
            target = random.choice(enemies)
        elif isinstance(source_player, Enemy):
            if len(players) == 0:
                return
            target = random.choice(players)
        hit_resistance = target.resistances["hit"]
        dmg_resistance = target.resistances["dmg"]
        attack_hits = calculate_hit(self.attack_action, hit_resistance)
        if not attack_hits:
            game.discord_connection.send_game_chat_sync(f"{source_player.combat_name} uses {self.attack_action.name}. It misses.")
            return
        damage_to_assign = calculate_damage(self.attack_action, dmg_resistance)
        assign_damage_response = target.assign_damage(game, source_player, target, damage_to_assign)
        game.discord_connection.send_game_chat_sync(f"{source_player.combat_name} uses {self.attack_action.name}. "+assign_damage_response)
        game.trigger("attack_hit", source=source_player, target=target, damage=damage_to_assign)
