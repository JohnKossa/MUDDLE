from __future__ import annotations
import discord

from typing import Optional

import Game

from game_objects.Commands.NoncombatCommands.NoncombatCommand import NoncombatCommand
from utils.ListHelpers import get_by_index


class TalkCommand(NoncombatCommand):
    def __init__(self):
        super().__init__()
        self.aliases = ["Talk", "TalkTo"]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Starts a conversation with the named NPC.",
            "If no name is provided, and only 1 NPC in the current room, conversation will be started with that NPC",
            "Params:",
            "  0: NPC name"
        ])

    def do_action(self, game: Game, params: list[str], message: discord.Message) -> str:
        from discord_objects.DiscordUser import UserUtils
        from game_objects.Conversation import Conversation
        player = UserUtils.get_character_by_username(str(message.author), game.discord_users)
        current_room = player.current_room
        npcs = current_room.get_npcs(game)
        npc_name = get_by_index(params, 0, None)
        if npc_name is None and len(npcs) == 1:
            chosen_npc = npcs[0]
        else:
            chosen_npc = next((npc for npc in npcs if npc.name == npc_name), None)
        if chosen_npc is None:
            return "Named person was not found"
        new_conversation = Conversation()
        new_conversation.npc = chosen_npc
        new_conversation.character = player
        new_conversation.room = current_room
        current_room.conversations.append(new_conversation)
        new_conversation.init_conversation(game, chosen_npc.dialog_tree)


class SayCommand(NoncombatCommand):
    def __init__(self):
        super().__init__()
        self.aliases = ["Say"]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Says the chosen response to the NPC",
            "Params:",
            "  0: Response Number"
        ])

    def do_action(self, game: Game, params: list[str], message: discord.Message) -> Optional[str]:
        from discord_objects.DiscordUser import UserUtils
        player = UserUtils.get_character_by_username(str(message.author), game.discord_users)
        current_room = player.current_room
        conversations = current_room.conversations
        my_conversation = next((conversation for conversation in conversations if conversation.character == player), None)
        if my_conversation is None:
            raise Exception(f"Conversation is none")
        my_conversation.handle_response(game, params[0])