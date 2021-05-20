from __future__ import annotations
import discord
from typing import Any, List

import Game
from game_objects.Character.Character import Character
from game_objects.Commands.PartialCombatCommands.PartialCombatCommand import PartialCombatCommand
from utils.ListHelpers import get_by_index


class Take(PartialCombatCommand):
    from game_objects.CombatEntity import CombatEntity

    def __init__(self):
        super().__init__()
        self.aliases: List[str] = [
            "Take",
            "Pickup"
        ]
        self.combat_action_cost: int = 1

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Picks up an item in the current room and adds it to your bag.",
            "Combat Params:",
            "    0: Item Name",
            "Noncombat Params:",
            "    0: Item Name or all (optional)"
        ])

    def command_valid(self, game: Game, source_player: CombatEntity, params: List[Any]) -> bool:
        from utils.CommandHelpers import match_item
        room = source_player.current_room
        matched_item = match_item(room.items, params)
        if matched_item is None:
            return False
        return True

    def do_noncombat(self, game: Game, params: List[str], message: discord.Message) -> str:
        from discord_objects.DiscordUser import UserUtils
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        player = discord_user.current_character
        room = player.current_room
        items = room.items
        target_item_name = get_by_index(params, 0, None)
        if (target_item_name is None) or (target_item_name.lower() == "all"):
            if len(items) == 0:
                return "Nothing to pick up."
            pickup_strings = []
            for item in items:
                player.inventory.add_item_to_bag(item)
                pickup_strings.append(f"Picked up {item.quantity} {item.name}")
            room.items = []
            return "\n".join(pickup_strings)
        else:
            matched_item = next((x for x in items if x.name.lower() == target_item_name.lower()), None)
            # matched_item = next(filter(lambda x: x.name.lower() == target_item_name.lower(), items), None)
            if matched_item is None:
                return "Item not found"
            player.inventory.add_item_to_bag(matched_item)
            room.items.remove(matched_item)
            return f"Picked up {matched_item.quantity} {matched_item.name}"

    def do_combat_action(self, game: Game, source_player: Character, params: List[Any]):
        target_item = params[0]
        room = source_player.current_room
        items = room.items
        matched_item = next((x for x in items if x.name.lower() == target_item.lower()), None)
        if matched_item is None:
            game.discord_connection.send_game_chat_sync(f"{source_player.combat_name} attempted to pick up a picked up  a {target_item} but could not find any.")
            return
        source_player.inventory.add_item_to_bag(matched_item)
        room.items.remove(matched_item)
        game.discord_connection.send_game_chat_sync(f"{source_player.combat_name} picked up {matched_item.quantity} {matched_item.name}")
