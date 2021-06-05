import discord

import Game
from game_objects.Commands.Command import Command


class ListCommands(Command):
    def __init__(self):
        super().__init__()
        self.aliases = [
            "ListCommands",
            "Commands"
        ]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Lists all commands currently available to you",
            "Params: None"
        ])

    def do_action(self, game: Game, params: list[str], message: discord.Message) -> str:
        from discord_objects.DiscordUser import UserUtils
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        if discord_user is None:
            return "You are not listed as a user in this game."
        commands = discord_user.get_commands(game)
        command_aliases = [x.default_alias() for x in commands]
        command_aliases.sort()
        return "Your commands are:\n{}".format("\n".join(command_aliases))