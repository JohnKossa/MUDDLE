class Command:
    aliases = []
    combat_action_cost = 0

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
    combat_action_cost = 0

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
    combat_action_cost = 0

    @staticmethod
    def do_action(game, params, message):
        return str(game.maze)


class Drop(Command):
    aliases = [
        "Drop"
        "Discard"
    ]
    combat_action_cost = 0

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
        "Rebuild"
    ]
    combat_action_cost = 0

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

    @staticmethod
    def do_action(game, params, message):
        from game_objects.Player import Player
        from discord_objects.DiscordUser import UserUtils, DiscordUser
        new_player = Player()
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
        target_player.current_room = door
        return str(target_player.current_room)