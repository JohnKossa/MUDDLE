from __future__ import annotations
import discord

import Game

from game_objects.Commands.NoncombatCommands.NoncombatCommand import NoncombatCommand
from utils.ListHelpers import get_by_index


class Unequip(NoncombatCommand):
    def __init__(self):
        super().__init__()
        self.aliases = ["Unequip"]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Unequips an equipped item from the named slot and adds it back to your bag",
            "Params:",
            "    0: Slot Name"
        ])

    def do_action(self, game: Game, params: list[str], message: discord.Message) -> str:
        from discord_objects.DiscordUser import UserUtils
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        player = discord_user.current_character
        slot = get_by_index(params, 0)
        worked, response = player.inventory.unequip_item(slot)
        if worked:
            return f"Unequipped item from {slot}"
        else:
            return response
