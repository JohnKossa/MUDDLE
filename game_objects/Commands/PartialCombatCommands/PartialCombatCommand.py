from __future__ import annotations
import discord
from typing import Any, List

import Game
from game_objects.Character.Character import Character
from game_objects.Commands.Command import Command


class PartialCombatCommand(Command):
    def __init__(self):
        super().__init__()

    def do_action(self, game: Game, params: List[str], message: discord.Message) -> str:
        from discord_objects.DiscordUser import UserUtils
        target_player = UserUtils.get_character_by_username(str(message.author), game.discord_users)
        if target_player is None:
            return "You don't currently have a character. Use the !NewCharacter command to create one."
        room = target_player.current_room
        if room.combat is None:
            return self.do_noncombat(game, params, message)
        else:
            return self.enqueue_order(game, target_player, params)

    def command_valid(self, game: Game, source_player: Character, params: List[Any]) -> bool:
        """Check if the command is still valid."""
        return True

    def do_noncombat(self, game: Game, params: List[str], message: discord.Message) -> str:
        return ""

    def do_combat_action(self, game: Game, source_player: Character, params: List[Any]) -> None:
        pass

    def enqueue_order(self, game: Game, target_player: Character, params: List[Any]) -> str:
        room = target_player.current_room
        room.combat.accept_player_order(game, target_player, self.do_combat_action, params, self.combat_action_cost)
        to_return = "Order Accepted."
        if room.combat is not None:
            action_count = room.combat.sum_actions_for_entity(target_player)
            remaining_actions = target_player.actions - action_count
            if 0 < remaining_actions < target_player.actions:
                to_return = to_return + f"You have {remaining_actions} action points remaining."
        return to_return
