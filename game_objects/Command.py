def all_commands():
    import sys
    import inspect
    command_list = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and issubclass(obj, Command):
            command_list = command_list + [obj]
    return command_list


class Command:
    aliases = []
    combat_action_cost = 0

    @classmethod
    def default_alias(cls):
        if len(cls.aliases) == 0:
            return None
        return cls.aliases[0]

    @classmethod
    def show_help(cls):
        help_text = "No help text has been set for this command. Known aliases for this command are: "
        help_text = help_text + " , ".join(cls.aliases)
        return help_text

    @classmethod
    def command_name(cls):
        return cls.__name__

    @staticmethod
    def do_action(game, params, message):
        raise Exception("No action implemented for command")


class ShowHelp(Command):
    aliases = [
        "ShowHelp",
        "Help"
    ]

    @classmethod
    def show_help(cls):
        return "\n".join([
            "Gives details about the usage of the named command",
            "Params:",
            "    0: Command Name"
        ])

    @staticmethod
    def do_action(game, params, message):
        if len(params) == 0:
            return ShowHelp.show_help()
        supplied_alias = params[0].lower()
        for command in all_commands():
            lower_aliases = [x.lower() for x in command.aliases]
            if supplied_alias in lower_aliases:
                return command.show_help()


class ShowAliases(Command):
    aliases = [
        "ShowAliases",
        "Alias"
    ]

    @classmethod
    def show_help(cls):
        return "\n".join([
            "Gives details about the usage of the named command",
            "Params:",
            "    0: Command Name"
        ])

    @staticmethod
    def do_action(game, params, message):
        if len(params) == 0:
            return
        supplied_alias = params[0].lower()
        for command in all_commands():
            lower_aliases = [x.lower() for x in command.aliases]
            if supplied_alias in lower_aliases:
                return "Known aliases for {}:\n".format(command.command_name())+("\n".join(command.aliases))


class ListCommands(Command):
    aliases = [
        "ListCommands",
        "Commands"
    ]
    combat_action_cost = 0

    @classmethod
    def show_help(cls):
        return "\n".join([
            "Lists all commands currently available to you",
            "Params: None"
        ])

    @staticmethod
    def do_action(game, params, message):
        from discord_objects.DiscordUser import UserUtils
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        if discord_user is None:
            return "You are not listed as a user in this game."
        commands = discord_user.get_commands()
        command_aliases = [x.default_alias() for x in commands]
        command_aliases.sort()
        return "Your commands are:\n{}".format("\n".join(command_aliases))


class ShowMap(Command):
    aliases = [
        "ShowMap",
        "Map"
    ]
    combat_action_cost = 0

    @classmethod
    def show_help(cls):
        return "\n".join([
            "Debug command: Displays the current map",
            "Params: None"
        ])

    @staticmethod
    def do_action(game, params, message):
        return str(game.maze)


class Drop(Command):
    aliases = [
        "Drop"
        "Discard"
    ]
    combat_action_cost = 0

    @classmethod
    def show_help(cls):
        return "\n".join([
            "Not yet implemented: Will drop a held or stored item on the floor of the current room ",
            "Params:",
            "    0: Item Name",
            "    1: (optional) Quantity"
        ])

    @staticmethod
    def do_action(game, params, message):
        # params -1 is item name
        # params 1 if present is quantity, default 1
        # remove quantity of the item from the player's inventory
        # add the item to the floor of the room
        pass


class RebuildMaze(Command):
    aliases = [
        "RebuildMaze",
        "Rebuild",
        "RebuildMap"
    ]
    combat_action_cost = 0

    @classmethod
    def show_help(cls):
        return "\n".join([
            "Debug Command: Regenerates the current maze and kicks all players back to the start",
            "Params:",
            "    0: Width",
            "    1: Height",
            "    2. Difficulty"
        ])

    @staticmethod
    def do_action(game, params, message):
        width = int(params[0])
        height = int(params[1])
        difficulty = int(params[2])
        game.init_maze(width, height, difficulty)
        return "Maze rebuilt!\n"+str(game.maze)


class NewCharacter(Command):
    aliases = [
        "NewCharacter",
        "NewChar",
        "MakeCharacter",
        "MakeChar"
    ]

    @classmethod
    def show_help(cls):
        return "\n".join([
            "Creates a new character, associates it with your user, and inserts it in the starting room of the maze",
            "Params: None"
        ])

    @staticmethod
    def do_action(game, params, message):
        from game_objects.Character import Character
        from discord_objects.DiscordUser import UserUtils, DiscordUser
        new_player = Character()
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        if discord_user is None:
            discord_user = DiscordUser(username=str(message.author), current_character=new_player)
        else:
            discord_user.current_character = new_player
        game.register_player(new_player)
        game.discord_users = game.discord_users + [discord_user]
        new_player.discord_user = discord_user
        return "New character created for {}".format(message.author)


class Exit(Command):
    aliases = [
        "Exit",
        "Go",
        "Door"
    ]

    @classmethod
    def show_help(cls):
        return "\n".join([
            "Moves your character through the named exit",
            "Params:",
            "    0: The name of the door to use"
        ])

    @staticmethod
    def do_action(game, params, message):
        from discord_objects.DiscordUser import UserUtils
        target_player = UserUtils.get_character_by_username(str(message.author), game.discord_users)
        if target_player is None:
            return "You don't currently have a character. Use the !NewCharacter command to create one."
        room = target_player.current_room
        direction = params[0]
        door = room.get_door(direction.lower())
        if door is None:
            return "Invalid direction. Room has no {} exit.".format(direction)
        game.trigger("before_leave_room")
        game.trigger("before_enter_room")
        target_player.current_room = door
        game.trigger("after_leave_room")
        game. trigger("after_enter_room")
        return str(target_player.current_room)