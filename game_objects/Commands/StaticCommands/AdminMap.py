from typing import List

import discord

import Game
from game_objects.Commands.Command import Command


class AdminMap(Command):
    def __init__(self):
        super().__init__()
        self.aliases = [
            "AdminMap"
        ]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Debug command: Displays the current map",
            "Params: None"
        ])

    def do_action(self, game: Game, params: List[str], message: discord.Message) -> str:
        from discord_objects.DiscordUser import UserUtils
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        if discord_user.is_admin:
            return game.maze.admin_map(game)
        return "You are not an admin!"