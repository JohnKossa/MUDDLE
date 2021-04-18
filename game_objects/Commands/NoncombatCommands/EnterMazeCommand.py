from __future__ import annotations
import discord

from typing import List

import Game

from game_objects.Commands.NoncombatCommands.NoncombatCommand import NoncombatCommand


class EnterMazeCommand(NoncombatCommand):
    def __init__(self):
        super().__init__()
        self.aliases = ["EnterMaze"]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Enters the maze",
            "Params: None"
        ])

    def do_action(self, game: Game, params: List[str], message: discord.Message) -> str:
        from discord_objects.DiscordUser import UserUtils
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        player = discord_user.current_character
        player.zone = "Labyrinth"
        player.current_room = game.maze.entry_room
        return "You enter the maze.\n" + player.current_room.describe(game)
