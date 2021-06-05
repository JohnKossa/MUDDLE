from __future__ import annotations
import discord

import Game
from game_objects.Commands.NoncombatCommands.NoncombatCommand import NoncombatCommand


class ExitMaze(NoncombatCommand):
    def __init__(self):
        super().__init__()
        self.aliases = ["ExitMaze", "LeaveMaze"]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Leaves the current maze and returns to the town",
            "Params: None"
        ])

    def do_action(self, game: Game, params: list[str], message: discord.Message) -> str:
        from discord_objects.DiscordUser import UserUtils
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        player = discord_user.current_character
        player.zone = "Town"
        player.current_room = game.town.entry_room
        return "You leave the maze.\n" + player.current_room.describe(game)
