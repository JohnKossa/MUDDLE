from __future__ import annotations
import discord
from typing import Any

from Game import Game
from game_objects.Character.Character import Character
from game_objects.Commands.PartialCombatCommands.PartialCombatCommand import PartialCombatCommand
from utils.ListHelpers import get_by_index


class Cast(PartialCombatCommand):
    from game_objects.CombatEntity import CombatEntity

    def __init__(self):
        super().__init__()
        self.aliases: list[str] = [
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

    def command_valid(self, game: Game, source_player: CombatEntity, params: list[Any]) -> bool:
        """Check if the command is still valid."""
        from utils.CommandHelpers import match_spell
        from utils.Constanats import EquipmentSlots
        target_spell = get_by_index(params, 0)
        if target_spell is None:
            return False
        matched_spell = match_spell(source_player.known_spells, params)
        if matched_spell is None and isinstance(source_player, Character):
            from game_objects.Items.Spellbook import Spellbook
            offhand_item = source_player.inventory.equipment[EquipmentSlots.Offhand]
            if offhand_item is not None and isinstance(offhand_item, Spellbook):
                matched_spell = match_spell(source_player.inventory.equipment[EquipmentSlots.Offhand].spells, params)
            elif matched_spell is not None and source_player.inventory.equipment[EquipmentSlots.Mainhand] is not None and isinstance(source_player.inventory.equipment[EquipmentSlots.Mainhand], Spellbook):
                matched_spell = match_spell(source_player.inventory.equipment[EquipmentSlots.Mainhand].spells, params)
        if matched_spell is None:
            return False
        if not matched_spell.usable_in_combat:
            return False
        # TODO
        # get target type from spell
        # attempt to match from target types in room
        # if all targets valid
        return True

    def do_noncombat(self, game: Game, params: list[str], message: discord.Message):
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

    def do_combat_action(self, game: Game, source_player: Character, params: list[Any]) -> None:
        from utils.CommandHelpers import match_spell
        from utils.Constanats import EquipmentSlots
        target_spell = get_by_index(params, 0)
        if target_spell is None:
            game.discord_connection.send_game_chat_sync(f"{source_player.combat_name} attempted to cast a spell.")
            return
        matched_spell = match_spell(source_player.known_spells, params)
        if matched_spell is None and isinstance(source_player, Character):
            from game_objects.Items.Spellbook import Spellbook
            offhand_item = source_player.inventory.equipment[EquipmentSlots.Offhand]
            mainhand_item = source_player.inventory.equipment[EquipmentSlots.Mainhand]
            if offhand_item is not None and isinstance(offhand_item, Spellbook):
                matched_spell = match_spell(offhand_item.spells, params)
            elif matched_spell is not None and mainhand_item is not None and isinstance(mainhand_item, Spellbook):
                matched_spell = match_spell(mainhand_item.spells, params)
        if matched_spell is None:
            game.discord_connection.send_game_chat_sync(
                f"{source_player.combat_name} attempted to cast {target_spell} but can't remember how.")
            return
        if not matched_spell.usable_in_combat:
            game.discord_connection.send_game_chat_sync(
                f"{source_player.combat_name} attempted to cast {target_spell} but can't do so while in combat.")
            return
        #   if all targets valid
        #       do it
