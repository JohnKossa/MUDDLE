from __future__ import annotations
from typing import Any

import Game
from game_objects.Commands.CombatCommands.CombatCommand import CombatOnlyCommand


class PassCommand(CombatOnlyCommand):
    from game_objects import Character

    def __init__(self):
        super().__init__()
        self.aliases: list[str] = ["Pass"]

    def do_combat_action(self, game: Game, source_player: Character, params: list[Any]):
        source_player.health += (source_player.max_health - source_player.health)*.05
        source_player.stamina += (source_player.max_stamina - source_player.stamina)*.05
        source_player.mana += (source_player.max_mana - source_player.mana)*.05
        game.discord_connection.send_game_chat_sync(f"{source_player.name} passes. Stats partially restored.")
