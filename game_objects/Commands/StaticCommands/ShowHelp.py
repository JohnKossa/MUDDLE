import discord

import Game
from game_objects.Commands.Command import Command
from utils.ListHelpers import get_by_index


class ShowHelp(Command):
    # TODO Broken because of moving commands into their own directories
    def __init__(self):
        super().__init__()
        self.aliases = [
            "ShowHelp",
            "Help"
        ]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Gives details about the usage of the named command",
            "Params:",
            "    0: Command Name"
        ])

    def do_action(self, game: Game, params: list[str], message: discord.Message) -> str:
        if len(params) == 0:
            return ShowHelp.show_help()
        from discord_objects.DiscordUser import UserUtils
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        if discord_user is None:
            return "You are not listed as a user in this game."
        supplied_alias = get_by_index(params, 0).lower()
        for command in discord_user.get_commands(game):
            lower_aliases = [x.lower() for x in command.aliases]
            if supplied_alias in lower_aliases:
                return command.show_help()