from __future__ import annotations

import random
from typing import Any, List

import Game

from game_objects.Commands.CombatCommands.CombatCommand import CombatOnlyCommand
from utils.CombatHelpers import calculate_damage


class AttackCommand(CombatOnlyCommand):
    from game_objects.Character import Character
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

    def do_combat_action(self, game: Game, source_player: Character, params: List[Any]) -> None:
        from game_objects.Character import Character
        from game_objects.Enemy import Enemy
        enemies = source_player.current_room.combat.enemies
        players = source_player.current_room.combat.players
        target = None
        if len(params):
            for enemy in enemies:
                if enemy.name == params[0]:
                    target = enemy
            for player in players:
                if player.name == params[0]:
                    target = player
        elif type(source_player) is Character:
            if len(enemies) == 0:
                return
            target = random.choice(enemies)
        elif type(source_player) is type(Enemy) or issubclass(type(source_player), type(Enemy)):
            if len(players) == 0:
                return
            target = random.choice(players)
        hit_resistance = target.resistances["hit"]
        dmg_resistance = target.resistances["dmg"]
        damage = calculate_damage(self.attack_action, hit_resistance, dmg_resistance)
        output = f"{source_player.name} uses {self.attack_action.name}. "
        output = output + ("It misses." if damage == 0 else f"{target.name} takes {damage} damage.")
        game.discord_connection.send_game_chat_sync(output)
        target.health = max(0, target.health-damage)