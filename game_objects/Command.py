class Command:
    aliases = []

    @classmethod
    def default_alias(cls):
        if len(cls.aliases) == 0:
            return None
        return cls.aliases[0]

    @classmethod
    def command_name(cls):
        return cls.__name__

    @staticmethod
    def do_action(game, params, message):
        raise Exception("No action implemented for command")


class ListCommands(Command):
    aliases = [
        "ListCommands"
    ]

    @staticmethod
    def do_action(game, params, message):
        from discord_objects.DiscordUser import UserUtils
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        if discord_user is None:
            return "You are not listed as a user in this game."
        commands = discord_user.get_commands()
        command_aliases = [x.default_alias() for x in commands]
        return "Your commands are:\n{}".format("\n".join(command_aliases))


class ShowMap(Command):
    aliases = [
        "ShowMap",
        "Map"
    ]

    @staticmethod
    def do_action(game, params, message):
        return str(game.maze)


class RebuildMaze(Command):
    aliases = [
        "RebuildMaze",
        "Rebuild"
    ]

    @staticmethod
    def do_action(game, params, message):
        width = int(params[0])
        height = int(params[1])
        difficulty = int(params[2])
        game.init_maze(width, height, difficulty)
        return "Maze rebuilt!\n"+str(game.maze)
