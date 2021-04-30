from typing import List

import discord

import Game
from game_objects.Commands.Command import Command


class LookCommand(Command):
    def __init__(self):
        super().__init__()
        self.aliases = ["Look", "Inspect", "Perception"]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Look around the room",
            "Params: None"
        ])

    def do_action(self, game: Game, params: List[str], message: discord.Message) -> str:
        from discord_objects.DiscordUser import UserUtils
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        player = discord_user.current_character
        return player.current_room.describe(game)