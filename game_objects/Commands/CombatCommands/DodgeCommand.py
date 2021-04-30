from __future__ import annotations
from typing import Any, List

from Game import Game
from game_objects.Character.Character import Character
from game_objects.Commands.CombatCommands.CombatCommand import CombatOnlyCommand


class DodgeCommand(CombatOnlyCommand):
    def __init__(self, aliases: List[str] = None):
        super().__init__()
        self.combat_action_cost: int = 1
        if aliases is not None:
            self.aliases: List[str] = aliases
        else:
            self.aliases: List[str] = ["Dodge"]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Attempts to dodge attacks until the beginning of your next turn.",
            "Costs 10 stamina to use.",
            "Params: None"
        ])

    def do_combat_action(self, game: Game, source_player: Character, params: List[Any]) -> None:
        from game_objects.Status.DodgeStatus import DodgeStatus
        if source_player.stamina < 5:
            game.discord_connection.send_game_chat_sync(f"{source_player.combat_name}'s stamina is too low.")
        else:
            source_player.stamina = source_player.stamina - 5
            game.discord_connection.send_game_chat_sync(f"{source_player.combat_name} dodges.")
            status = DodgeStatus(source_player)
            status.attach_triggers(game)
            source_player.status_effects.append(status)
