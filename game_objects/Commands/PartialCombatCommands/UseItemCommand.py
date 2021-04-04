from __future__ import annotations
import discord
from typing import Any, List

from Game import Game
from game_objects.Character.Character import Character
from game_objects.Commands.PartialCombatCommands.PartialCombatCommand import PartialCombatCommand


class UseItem(PartialCombatCommand):
    def __init__(self):
        super().__init__()
        self.aliases: List[str] = [
            "UseItem",
            "Use",
        ]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Performs the default action of an item.",
            "If in combat, only works for equipped items",
            "If out of combat, works for any stored items as well",
            "Params:",
            "    0: The name of the item to use"
        ])

    def do_noncombat(self, game: Game, params: List[str], message: discord.Message) -> str:
        # look for matched item in belt then bag, calling use_effect on it
        # TODO Check if item quantity is greater than 0 before using
        # TODO check if item quantity is less than 0 after
        from discord_objects.DiscordUser import UserUtils
        from utils.ListHelpers import get_by_index
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        player = discord_user.current_character
        item_name = get_by_index(params, 0, None)
        if item_name is None:
            return "Item name not specified. Usage is:\n" + UseItem.show_help()
        matched_item = player.inventory.get_belt_item_by_name(item_name)
        source_container = "belt"
        if matched_item is None:
            matched_item = player.inventory.get_bag_item_by_name(item_name)
            source_container = "bag"
        if matched_item is None:
            return f"{item_name} was not found on belt or in bags"
        matched_item.use_effect(game, player, params[1:])
        matched_item.quantity = matched_item.quantity-1
        if matched_item.quantity == 0:
            if source_container == "belt":
                player.inventory.equipment["belt"].remove(matched_item)
            elif source_container == "bag":
                player.inventory.bag.remove(matched_item)
        return f"{item_name} used"

    def do_combat_action(self, game: Game, source_player: Character, params: List[Any]) -> None:
        # look for a matched item in belt only, calling use_effect on it
        # look for matched item in belt then bag, calling use_effect on it
        from utils.ListHelpers import get_by_index
        item_name = get_by_index(params, 0, None)
        if item_name is None:
            game.discord_connection.send_game_chat_sync("Item name not specified. Usage is:\n" + UseItem.show_help(), [source_player.discord_user])
        matched_item = source_player.inventory.get_belt_item_by_name(item_name)
        if matched_item is None:
            game.discord_connection.send_game_chat_sync(f"{item_name} was not found on belt", [source_player.discord_user])
        matched_item.use_effect(game, source_player, params[1:])
        matched_item.quantity = matched_item.quantity - 1
        if matched_item.quantity == 0:
            source_player.inventory.equipment["belt"].remove(matched_item)
