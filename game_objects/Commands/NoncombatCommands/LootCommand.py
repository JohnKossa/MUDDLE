from __future__ import annotations
import discord
from typing import List

import Game

from game_objects.Commands.NoncombatCommands.NoncombatCommand import NoncombatCommand
from utils.ListHelpers import get_by_index
from utils.TextHelpers import enumerate_objects


class LootCommand(NoncombatCommand):
    def __init__(self):
        super().__init__()
        self.aliases = ["Loot"]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Loots items from the named object.",
            "Params:",
            "    0: Object Name"
        ])

    def do_action(self, game: Game, params: List[str], message: discord.Message) -> str:
        from discord_objects.DiscordUser import UserUtils
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        player = discord_user.current_character
        room = player.current_room
        object_name = get_by_index(params, 0, None)
        if object_name is None:
            return "No object specified to loot. Usage is:\n"+LootCommand.show_help()
        matched_object = next(filter(lambda fixture: fixture.name.lower() == object_name.lower() and hasattr(fixture, "items"), room.fixtures), None)
        if matched_object is None:
            return f"Lootable object {object_name} not found."
        looted_items = matched_object.items
        matched_object.items = []
        if len(looted_items) == 0:
            return f"{object_name.capitalize()} was empty."
        player.inventory.bag = player.inventory.bag + looted_items
        text_described_items = [f"{x.quantity}x {x.name}" for x in looted_items]
        return f"Picked up {enumerate_objects(text_described_items)}"
