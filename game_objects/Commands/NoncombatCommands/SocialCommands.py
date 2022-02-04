from __future__ import annotations
import discord

from typing import Optional

import Game

from game_objects.Commands.NoncombatCommands.NoncombatCommand import NoncombatCommand
from utils.ListHelpers import get_by_index


class HighFiveCommand(NoncombatCommand):
    def __init__(self):
        super().__init__()
        self.aliases = ["HighFive", "High5", "HiFive", "Hi5"]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Gives a high five to the named player character",
            "If no name is provided, and only 1 other player is in the current room, high five will be targeted to them",
            "Params:",
            "  0: Player name"
        ])

    def do_action(self, game: Game, params: list[str], message: discord.Message) -> str:
        from discord_objects.DiscordUser import UserUtils
        player = UserUtils.get_character_by_username(str(message.author), game.discord_users)
        current_room = player.current_room
        players = current_room.get_characters(game)
        player_name = get_by_index(params, 0, None)
        if player_name is None and len(players) == 2:
            chosen_player = players[0] if players[0] != player else players[1]
        elif player_name is None and len(players) >= 2:
            return "You're left hanging."
        else:
            chosen_player = next((x for x in players if x.name.replace(" ","").lower() == player_name.replace(" ","").lower()), None)
        if chosen_player is None:
            return "Named person was not found"
        return f"You give an epic high five to {chosen_player.name}"
