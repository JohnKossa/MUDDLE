from __future__ import annotations
import discord
from typing import Any, List

from Game import Game
from game_objects.Character.Character import Character
from game_objects.Commands.PartialCombatCommands.PartialCombatCommand import PartialCombatCommand
from utils.ListHelpers import get_by_index


class Cast(PartialCombatCommand):
    from game_objects.CombatEntity import CombatEntity

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

    def command_valid(self, game: Game, source_player: CombatEntity, params: List[Any]) -> bool:
        """Check if the command is still valid."""
        from utils.CommandHelpers import match_spell
        from utils.Constanats import EquipmentSlots
        target_spell = get_by_index(params, 0)
        if target_spell is None:
            return False
        matched_spell = match_spell(source_player.known_spells, params)
        if matched_spell is None and isinstance(source_player, Character):
            from game_objects.Items.Spellbook import Spellbook
            if source_player.inventory.equipment[EquipmentSlots.Offhand] is not None and isinstance(source_player.inventory.equipment[EquipmentSlots.Offhand], Spellbook):
                matched_spell = match_spell(source_player.inventory.equipment[EquipmentSlots.Offhand].spells, params)
            elif matched_spell is not None and source_player.inventory.equipment[EquipmentSlots.Mainhand] is not None and isinstance(source_player.inventory.equipment[EquipmentSlots.Mainhand], Spellbook):
                matched_spell = match_spell(source_player.inventory.equipment[EquipmentSlots.Mainhand].spells, params)
        if matched_spell is None:
            return False
        if not matched_spell.usable_in_combat:
            return False
        # get target type from spell
        # attempt to match from target types in room
        # if all targets valid
        return True

    def do_noncombat(self, game: Game, params: List[str], message: discord.Message):
        from discord_objects.DiscordUser import UserUtils
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        player = discord_user.current_character
        target_spell = get_by_index(params, 0)
        if target_spell is None:
            return Cast.show_help()
        # attempt to match from known spells
        # if spellbook in mainhand or offhand
        #   attempt to match from spellbook
        # if spell can be used out of combat
        #   get target type from spell
        #   attempt to match from target types in room
        #   if all targets valid
        #       do it
        return "Not Implemented"

    def do_combat_action(self, game: Game, source_player: Character, params: List[Any]) -> None:
        target_spell = params[0]
        # attempt to match from known spells
        # if spellbook in mainhand or offhand
        #   attempt to match from spellbook
        # if spell can be used in combat
        #   get target type from spell
        #   attempt to match from target types in room
        #   if all targets valid
        #       do it
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
