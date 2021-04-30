from __future__ import annotations
import discord
from typing import Any, List

import Game
from game_objects.Commands.Command import Command


class CombatOnlyCommand(Command):
    from game_objects.Character.Character import Character

    def __init__(self):
        super().__init__()
        self.combat_action_cost: int = 1

    def command_valid(self, game: Game, source_player: Character, params: List[Any]) -> bool:
        """Check if the command is still valid."""
        return True

    def do_action(self, game: Game, params: List[str], message: discord.Message) -> str:
        from discord_objects.DiscordUser import UserUtils
        user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        character = user.current_character
        room = character.current_room
        combat = room.combat
        combat.accept_player_order(game, character, self.do_combat_action, params, self.combat_action_cost)
        action_count = combat.sum_actions_for_entity(character)
        remaining_actions = character.actions - action_count
        return "Order Accepted." + (f"You have {remaining_actions} action points remaining." if 0 < remaining_actions < character.actions else "")

    def do_combat_action(self, game: Game, source_player: Character, params: List[Any]) -> None:
        raise Exception("Not yet implemented")
