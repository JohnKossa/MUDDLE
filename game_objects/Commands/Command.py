from __future__ import annotations
from typing import List, Optional
import discord

import Game

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

    def do_action(self, game: Game, params: List[str], message: discord.Message) -> str:
        raise Exception("No action implemented for command")


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

    def do_action(self, game: Game, params: List[str], message: discord.Message) -> str:
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


class ShowAliases(Command):
    # TODO Broken because of moving commands into their own directories
    def __init__(self):
        super().__init__()
        self.aliases = [
            "ShowAliases",
            "Alias"
        ]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Gives details about the usage of the named command",
            "Params:",
            "    0: Command Name"
        ])

    def do_action(self, game: Game, params: List[str], message: discord.Message) -> str:
        if len(params) == 0:
            return ""
        from discord_objects.DiscordUser import UserUtils
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        if discord_user is None:
            return "You are not listed as a user in this game."
        supplied_alias = get_by_index(params, 0).lower()
        for command in discord_user.get_commands(game):
            lower_aliases = [x.lower() for x in command.aliases]
            if supplied_alias in lower_aliases:
                return f"Known aliases for {command.command_name()}:\n"+("\n".join(command.aliases))


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

    def do_action(self, game: Game, params: List[str], message: discord.Message) -> str:
        from discord_objects.DiscordUser import UserUtils
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        if discord_user is None:
            return "You are not listed as a user in this game."
        commands = discord_user.get_commands(game)
        command_aliases = [x.default_alias() for x in commands]
        command_aliases.sort()
        return "Your commands are:\n{}".format("\n".join(command_aliases))


class ShowMap(Command):
    def __init__(self):
        super().__init__()
        self.aliases = [
            "ShowMap",
            "Map"
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
        player = discord_user.current_character
        return game.maze.player_map(game, player)


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

    def do_action(self, game: Game, params: List[str], message: discord.Message) -> str:
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

    def do_action(self, game: Game, params: List[str], message: discord.Message) -> str:
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
            f"HP: {player.health}/{player.max_health}",
            f"PP: {player.stamina}/{player.max_stamina}",
            f"MP {player.mana}/{player.max_mana}"
        ])
        if get_by_index(params, 0, "").lower() == "stats":
            to_return = to_return + "\n"
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


class InventoryCommand(Command):
    def __init__(self):
        super().__init__()
        self.aliases = ["Inventory", "Items", "Bag"]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Lists your equipped items and the contents of your bags.",
            "Params: None"
        ])

    def do_action(self, game: Game, params: List[str], message: discord.Message) -> str:
        from discord_objects.DiscordUser import UserUtils
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        player = discord_user.current_character
        player.inventory.consolidate_items()
        to_return = ""
        if len(player.inventory.equipment.values()) > 0:
            to_return = to_return + "Equipment:\n"
        for k, v in player.inventory.equipment.items():
            if v is not None and k != "belt":
                to_return = to_return + k.capitalize()+": "+v.name+"\n"
            if k == "belt" and len(v) > 0:
                to_return = to_return + "Belt:"
                for item_stack in player.inventory.equipment["belt"]:
                    to_return = to_return + f"\n{item_stack.quantity}x {item_stack.name}"
        if len(player.inventory.bag) > 0:
            to_return = to_return + "\nBag:"
        for item_stack in player.inventory.bag:
            to_return = to_return + f"\n{item_stack.quantity}x {item_stack.name}"
        return to_return
