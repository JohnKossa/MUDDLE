from typing import List

import discord

import Game
from game_objects.Commands.Command import Command
from utils.ListHelpers import get_by_index


class CharacterCommand(Command):
    def __init__(self):
        super().__init__()
        self.aliases = ["Character", "Char", "Player", "Status"]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Shows relevant stats about your current character.",
            "Params:",
            "    0: Stats(optional)"
        ])

    def do_action(self, game: Game, params: List[str], message: discord.Message) -> str:
        from discord_objects.DiscordUser import UserUtils
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        player = discord_user.current_character
        to_return = "\n".join([
            f"{player.name}",
            f"HP: {player.display_health}/{player.max_health}",
            f"PP: {player.display_stamina}/{player.max_stamina}",
            f"MP {player.display_mana}/{player.max_mana}"
        ])
        if get_by_index(params, 0, "").lower() == "stats":
            to_return = to_return + "\n"
            to_return = to_return + "Attack Bonuses:\n"
            to_return = to_return + f"  Hit: {player.hit_bonus}\n"
            to_return = to_return + f"  Dmg: {player.dmg_bonus}\n"
            player_resistances = player.resistances
            if len(player_resistances["hit"].keys()) > 0:
                to_return = to_return + "Hit Resistances:\n"
                for k, v in player_resistances["hit"].items():
                    to_return = to_return + f"  {k.capitalize()}: {v}\n"
            if len(player_resistances["dmg"].keys()) > 0:
                to_return = to_return + "Damage Resistances:\n"
                for k, v in player_resistances["dmg"].items():
                    to_return = to_return + f"  {k.capitalize()}: {v}\n"
        return to_return