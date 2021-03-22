from __future__ import annotations
from typing import Any, List

from Game import Game
from game_objects.Character import Character

from game_objects.Commands.CombatCommands.CombatCommand import CombatOnlyCommand


class BlockCommand(CombatOnlyCommand):
    def __init__(self, aliases: List[str] = None):
        super().__init__()
        self.combat_action_cost: int = 1
        if aliases is not None:
            self.aliases: List[str] = aliases
        else:
            self.aliases: List[str] = ["Block"]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Raises your shield and blocks attacks until your next turn.",
            "If you are hit, you will lose stamina instead of HP.",
            "Params: None",
        ])

    def do_combat_action(self, game: Game, source_player: Character, params: List[Any]) -> None:
        game.discord_connection.send_game_chat_sync(f"{source_player.name} raises their shield.")
        # TODO Implementation
        # add a "blocking" status to the player
        # add a trigger to remove the blocking status from the player at their next combat
        # modify combat cycle to have an "assign damage" step that allows for hooks to redirect damage
