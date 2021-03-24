from __future__ import annotations
import discord
from typing import Any, List

import Game
from game_objects.Character import Character
from game_objects.Commands.PartialCombatCommands.PartialCombatCommand import PartialCombatCommand
from utils.ListHelpers import get_by_index


class Exit(PartialCombatCommand):
    def __init__(self):
        super().__init__()
        self.aliases: List[str] = [
            "Exit",
            "Go",
            "Door"
        ]
        self.combat_action_cost: int = 2

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Moves your character through the named exit",
            "Params:",
            "    0: The name of the door to use"
        ])

    def do_noncombat(self, game: Game, params: List[str], message: discord.Message) -> str:
        from discord_objects.DiscordUser import UserUtils
        source_player = UserUtils.get_character_by_username(str(message.author), game.discord_users)
        if source_player is None:
            return "You don't currently have a character. Use the !NewCharacter command to create one."
        room = source_player.current_room
        direction = get_by_index(params, 0)
        door = room.get_door(direction.lower())
        if door is None:
            return f"Invalid direction. Room has no {direction} exit."
        old_room = source_player.current_room
        game.trigger("before_leave_room", source_player=source_player, room=old_room)
        game.trigger("before_enter_room", source_player=source_player, room=door)
        source_player.current_room = door
        game.trigger("leave_room", source_player=source_player, room=old_room)
        game.trigger("enter_room", source_player=source_player, room=source_player.current_room)
        return str(source_player.current_room)

    def do_combat_action(self, game: Game, source_player: Character, params: List[Any]) -> None:
        from Game import TriggerFunc
        # after combat finishes, leave room
        game.discord_connection.send_game_chat_sync(f"{source_player.combat_name} runs for the door.")
        game.once("round_end", TriggerFunc(self.leave_room, game, source_player, params))

    def leave_room(self, game: Game, source_player: Character, params: List[Any], **kwargs) -> None:
        discord_user = source_player.discord_user
        room = source_player.current_room
        direction = params[0]
        door = room.get_door(direction.lower())
        if door is None:
            game.discord_connection.send_game_chat_sync(f"Invalid direction. Room has no {direction} exit.", tagged_users=[discord_user])
            return
        old_room = source_player.current_room
        game.trigger("before_leave_room", source_player=source_player, room=old_room)
        game.trigger("before_enter_room", source_player=source_player, room=door)
        source_player.current_room = door
        game.trigger("leave_room", source_player=source_player, room=old_room)
        game.trigger("enter_room", source_player=source_player, room=source_player.current_room)
        return game.discord_connection.send_game_chat_sync(str(source_player.current_room), tagged_users=[discord_user])