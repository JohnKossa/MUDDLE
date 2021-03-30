from __future__ import annotations
import discord

from typing import List, Optional

from game_objects.Character.Character import Character
from game_objects.Commands.Command import Command, RebuildMaze, NewCharacter


class DiscordUser:
    def __init__(self, username: Optional[str] = None, current_character: Optional[Character] = None, discord_obj: Optional[discord.User] = None):
        self.username: str = username
        self.current_character: Character = current_character
        self.is_admin: bool = True if username == "kg959#1350" else False
        self.discord_obj: discord.User = discord_obj

    def get_commands(self) -> List[Command]:
        from game_objects.Commands.Command import ShowMap, ShowAliases, ListCommands, ShowHelp
        cmd_list = [ListCommands(), ShowAliases(), ShowMap(), ShowHelp()]
        if self.current_character is not None and not self.current_character.dead:
            cmd_list.extend(self.current_character.get_commands())
        else:
            cmd_list.append(NewCharacter())
        if self.is_admin:
            cmd_list.append(RebuildMaze())
        return cmd_list

    def __str__(self):
        return self.username


class UserUtils:
    @staticmethod
    def print_all(discord_users: List[DiscordUser]) -> None:
        print(" ".join([str(x) for x in discord_users]))

    @staticmethod
    def get_user_by_username(username: str, discord_users: List[DiscordUser]) -> Optional[DiscordUser]:
        for user in discord_users:
            if user.username == username:
                return user
        return None

    @staticmethod
    def get_character_by_username(username: str, discord_users: List[DiscordUser]) -> Optional[Character]:
        for user in discord_users:
            if user.username == username:
                return user.current_character
        return None
