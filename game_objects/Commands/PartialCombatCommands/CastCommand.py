from __future__ import annotations
import discord
from typing import Any, List

from Game import Game
from game_objects.Character.Character import Character
from game_objects.Commands.PartialCombatCommands.PartialCombatCommand import PartialCombatCommand
from utils.ListHelpers import get_by_index


class Cast(PartialCombatCommand):
    def __init__(self):
        super().__init__()
        self.aliases: List[str] = [
            "Cast",
            "Magic"
        ]
        self.combat_action_cost: int = 0

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Not yet implemented: Will cast a known spell",
            "Params:",
            "    0: Spell Name",
            "    1: Target"
        ])

    def do_noncombat(self, game: Game, params: List[str], message: discord.Message):
        # get character from user name
        # look up spell from known spells or from spellbook if one is equipped
        # if spell can be used out of combat
        #   check for valid targets
        #   if valid
        #       do it

        from discord_objects.DiscordUser import UserUtils
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        player = discord_user.current_character
        target_item = get_by_index(params, 0)
        if target_item is None:
            return Cast.show_help()
        room = player.current_room
        player_bag = player.inventory.bag
        matched_item = player.inventory.get_bag_item_by_name(target_item)
        if matched_item is None:
            return "Item not found"
        quantity = int(get_by_index(params, 1, "1"))
        quantity = max(quantity, matched_item.quantity)
        if quantity >= matched_item.quantity:
            room.items.append(matched_item)
            player_bag.remove(matched_item)
        else:
            dropped_items = matched_item.take_count_from_stack(quantity)
            room.items.append(dropped_items)
        return f"Dropped {quantity} {matched_item.name}"

    def do_combat_action(self, game: Game, source_player: Character, params: List[Any]) -> None:
        target_item = params[0]
        room = source_player.current_room
        player_bag = source_player.inventory.bag
        matched_item = source_player.inventory.get_bag_item_by_name(target_item)
        if matched_item is None:
            game.discord_connection.send_game_chat_sync(f"{source_player.combat_name} attempted to drop an item, but could find a {target_item} in their inventory")
            return
        quantity = get_by_index(params, 1, 1)
        quantity = max(quantity, matched_item.quantity)
        if quantity >= matched_item.quantity:
            room.items.append(matched_item)
            player_bag.remove(matched_item)
        else:
            dropped_items = matched_item.take_count_from_stack(quantity)
            room.items.append(dropped_items)
        game.discord_connection.send_game_chat_sync(f"{source_player.combat_name} dropped {quantity} {matched_item.name}")
