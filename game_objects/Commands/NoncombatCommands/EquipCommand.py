from __future__ import annotations
import discord

import Game

from game_objects.Commands.NoncombatCommands.NoncombatCommand import NoncombatCommand
from utils.ListHelpers import get_by_index


class Equip(NoncombatCommand):
    def __init__(self):
        super().__init__()
        self.aliases = ["Equip"]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Equips the named item from your bag in the named equipment slot",
            "Params:",
            "    0: Item Name",
            "    1: Slot Name"
        ])

    def do_action(self, game: Game, params: list[str], message: discord.Message) -> str:
        from discord_objects.DiscordUser import UserUtils
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        player = discord_user.current_character
        item_name = get_by_index(params, 0, None)
        if item_name is None:
            return "Item name not specified. Usage is:\n"+Equip.show_help()
        slot = get_by_index(params, 1, None)
        if slot is None:
            return "Slot not specified. Usage is:\n"+Equip.show_help()
        matched_item = player.inventory.get_bag_item_by_name(item_name)
        if matched_item is None:
            return "Item not found"
        success, err_reason = player.inventory.equip_item(matched_item, slot)
        if success:
            return "Item equipped"
        return err_reason
