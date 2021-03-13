def all_commands():
    import sys
    import inspect
    command_list = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and issubclass(obj, Command):
            command_list = command_list + [obj]
    return command_list


class Command:
    def __init__(self):
        self.combat_action_cost = 0
        self.aliases = []

    def default_alias(self):
        if len(self.aliases) == 0:
            return None
        return self.aliases[0]

    @classmethod
    def show_help(cls):
        return "No help text has been set for this command."

    @classmethod
    def command_name(cls):
        return cls.__name__

    def do_action(self, game, params, message):
        raise Exception("No action implemented for command")


class PartialCombatCommand(Command):
    def __init__(self):
        super().__init__()

    def do_action(self, game, params, message):
        from discord_objects.DiscordUser import UserUtils
        target_player = UserUtils.get_character_by_username(str(message.author), game.discord_users)
        if target_player is None:
            return "You don't currently have a character. Use the !NewCharacter command to create one."
        room = target_player.current_room
        if room.combat is None:
            return self.do_noncombat(game, params, message)
        else:
            return self.enqueue_order(game, target_player, params)

    def do_noncombat(self, game, params, message):
        return ""

    def do_combat_action(self, game, source_player, params):
        pass

    def enqueue_order(self, game, target_player, params):
        room = target_player.current_room
        room.combat.accept_player_order(game, target_player, self.do_combat_action, params, self.combat_action_cost)
        return "Order Accepted"


class ShowHelp(Command):
    def __init__(self):
        super().__init__()
        self.aliases = [
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

    def do_action(self, game, params, message):
        if len(params) == 0:
            return ShowHelp.show_help()
        supplied_alias = params[0].lower()
        for command in all_commands():
            lower_aliases = [x.lower() for x in command.aliases]
            if supplied_alias in lower_aliases:
                return command.show_help()


class ShowAliases(Command):
    def __init__(self):
        super().__init__()
        self.aliases = [
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

    def do_action(self, game, params, message):
        if len(params) == 0:
            return
        supplied_alias = params[0].lower()
        for command in all_commands():
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
    def show_help(cls):
        return "\n".join([
            "Lists all commands currently available to you",
            "Params: None"
        ])

    def do_action(self, game, params, message):
        from discord_objects.DiscordUser import UserUtils
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        if discord_user is None:
            return "You are not listed as a user in this game."
        commands = discord_user.get_commands()
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
    def show_help(cls):
        return "\n".join([
            "Debug command: Displays the current map",
            "Params: None"
        ])

    def do_action(self, game, params, message):
        return game.maze.player_map(game)


class Take(PartialCombatCommand):
    def __init__(self):
        super().__init__()
        self.aliases = [
            "Take",
            "Pickup"
        ]
        self.combat_action_cost = 1

    def show_help(cls):
        return "\n".join([
            "Picks up an item in the current room and adds it to your bag.",
            "Params:",
            "    0: Item Name",
        ])

    def do_noncombat(self, game, params, message):
        from discord_objects.DiscordUser import UserUtils
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        player = discord_user.current_character
        target_item = params[0]
        room = player.current_room
        items = room.items
        matched_item = next(filter(lambda  x: x.name.lower() == target_item.lower(), items), None)
        if matched_item is None:
            return "Item not found"
        player.inventory.bag[matched_item] = matched_item.quantity
        return f"Picked up {matched_item.quantity} {matched_item.name}"

    def do_combat_action(self, game, source_player, params):
        target_item = params[0]
        room = source_player.current_room
        items = room.items
        matched_item = next(filter(x for x in items if x.name.lower() == target_item.lower()), None)
        if matched_item is None:
            return "Item not found"
        source_player.inventory.bag[matched_item] = matched_item.quantity
        return f"{source_player.name} picked up {matched_item.quantity} {matched_item.name}"


class Drop(PartialCombatCommand):
    def __init__(self):
        super().__init__()
        self.aliases = [
            "Drop"
            "Discard"
        ]
        self.combat_action_cost = 0

    @classmethod
    def show_help(cls):
        return "\n".join([
            "Not yet implemented: Will drop a held or stored item on the floor of the current room ",
            "Params:",
            "    0: Item Name",
            "    1: (optional) Quantity"
        ])

    def do_noncombat(self, game, params, message):
        return ""

    def do_combat_action(self, game, source_player, params):
        pass


class RebuildMaze(Command):
    def __init__(self):
        super().__init__()
        self.aliases = [
            "RebuildMaze",
            "Rebuild",
            "RebuildMap"
        ]

    @classmethod
    def show_help(cls):
        return "\n".join([
            "Debug Command: Regenerates the current maze and kicks all players back to the start",
            "Params:",
            "    0: Width",
            "    1: Height",
            "    2. Difficulty"
        ])

    def do_action(self, game, params, message):
        width = int(params[0])
        height = int(params[1])
        difficulty = int(params[2])
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
    def show_help(cls):
        return "\n".join([
            "Creates a new character, associates it with your user, and inserts it in the starting room of the maze",
            "Params: None"
        ])

    def do_action(self, game, params, message):
        from game_objects.Character import Character
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


class Exit(PartialCombatCommand):
    def __init__(self):
        super().__init__()
        self.aliases = [
            "Exit",
            "Go",
            "Door"
        ]
        self.combat_action_cost = 2

    @classmethod
    def show_help(cls):
        return "\n".join([
            "Moves your character through the named exit",
            "Params:",
            "    0: The name of the door to use"
        ])

    def do_noncombat(self, game, params, message):
        from discord_objects.DiscordUser import UserUtils
        source_player = UserUtils.get_character_by_username(str(message.author), game.discord_users)
        if source_player is None:
            return "You don't currently have a character. Use the !NewCharacter command to create one."
        room = source_player.current_room
        direction = params[0]
        door = room.get_door(direction.lower())
        if door is None:
            return f"Invalid direction. Room has no {direction} exit."
        old_room = source_player.current_room
        game.trigger("before_leave_room", source_player=source_player, room=old_room)
        game.trigger("before_enter_room", source_player=source_player, room=door)
        source_player.current_room = door
        game.trigger("leave_room", source_player=source_player, room=old_room)
        game.trigger("enter_room", source_player=source_player, room=source_player.current_room)
        return str(source_player.current_room)

    def do_combat_action(self, game, source_player, params):
        from Game import TriggerFunc
        # after combat finishes, leave room
        game.discord_connection.send_game_chat_sync(f"{source_player.name} runs for the door.")
        game.once("round_end", TriggerFunc(self.leave_room, game, source_player, params))

    def leave_room(self, game, source_player, params, **kwargs):
        discord_user = source_player.discord_user
        room = source_player.current_room
        direction = params[0]
        door = room.get_door(direction.lower())
        if door is None:
            game.discord_connection.send_game_chat_sync(f"Invalid direction. Room has no {direction} exit.", tagged_users=[discord_user])
            return
        old_room = source_player.current_room
        game.trigger("before_leave_room", source_player=source_player, room=old_room)
        game.trigger("before_enter_room", source_player=source_player, room=door)
        source_player.current_room = door
        game.trigger("leave_room", source_player=source_player, room=old_room)
        game.trigger("enter_room", source_player=source_player, room=source_player.current_room)
        return game.discord_connection.send_game_chat_sync(str(source_player.current_room), tagged_users=[discord_user])


class UseItem(PartialCombatCommand):
    # check if in combat
    # if in combat:
    #   check equipped items for one patching params[0]
    #   if exists:
    #       call the use function on the item
    #   else:
    #       return "Item not found in currently equipped items."
    # else:
    #   check bagged items and then equipped items for one matching params[0]
    #   if exits:
    #       call the use function on the item
    #   else:
    #       return "Item not found in bag or equipped items
    def __init__(self):
        super().__init__()
        self.aliases = [
            "UseItem",
            "Use",
        ]

    @classmethod
    def show_help(cls):
        return "\n".join([
            "Performs the default action of an item.",
            "If in combat, only works for equipped items",
            "If out of combat, works for any stored items as well",
            "Params:",
            "    0: The name of the item to use"
        ])

    def do_noncombat(self, game, params, message):
        return ""

    def do_combat_action(self, game, source_player, params):
        pass
