from __future__ import annotations
from typing import List, Optional
import discord

from utils.ListHelpers import get_by_index


class Command:
    def __init__(self):
        self.combat_action_cost: int = 0
        self.aliases: List[str] = []

    def default_alias(self) -> Optional[str]:
        if len(self.aliases) == 0:
            return None
        return self.aliases[0]

    @classmethod
    def show_help(cls) -> str:
        return "No help text has been set for this command."

    @classmethod
    def command_name(cls) -> str:
        return cls.__name__

    def do_action(self, game: 'Game', params: List[str], message: discord.Message) -> str:
        raise Exception("No action implemented for command")


class RebuildMaze(Command):
    def __init__(self):
        super().__init__()
        self.aliases = [
            "RebuildMaze",
            "Rebuild",
            "RebuildMap"
        ]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Debug Command: Regenerates the current maze and kicks all players back to the start",
            "Params:",
            "    0: Width",
            "    1: Height",
            "    2. Difficulty"
        ])

    def do_action(self, game: 'Game', params: List[str], message: discord.Message) -> str:
        width = int(get_by_index(params, 0, "11"))
        height = int(get_by_index(params, 1, "11"))
        difficulty = int(get_by_index(params, 2, "6"))
        game.init_maze(width, height, difficulty)
        return "Maze rebuilt!\n"+str(game.maze)


class NewCharacter(Command):
    def __init__(self):
        super().__init__()
        self.aliases = [
            "NewCharacter",
            "NewChar",
            "MakeCharacter",
            "MakeChar"
        ]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Creates a new character, associates it with your user, and inserts it in the starting room of the maze",
            "Params: None"
        ])

    def do_action(self, game: 'Game', params: List[str], message: discord.Message) -> str:
        from game_objects.Character.Character import Character
        from discord_objects.DiscordUser import UserUtils, DiscordUser
        new_player = Character()
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        if discord_user is None:
            discord_user = DiscordUser(username=str(message.author), current_character=new_player, discord_obj=message.author)
        else:
            discord_user.current_character = new_player
        game.register_player(new_player)
        game.discord_users = game.discord_users + [discord_user]
        new_player.discord_user = discord_user
        return f"New character {new_player.name} created for {message.author}"


