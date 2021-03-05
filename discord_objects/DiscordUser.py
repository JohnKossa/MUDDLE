from game_objects.Command import Command


class DiscordUser:
    def __init__(self, username=None, current_character=None):
        self.username = username
        self.current_character = current_character
        self.is_admin = True if username == "kg959#1350" else False

    def get_commands(self):
        from game_objects.Command import ShowMap, ListCommands
        cmd_list = [ListCommands, ShowMap]
        if self.current_character is not None:
            cmd_list = cmd_list + self.current_character.get_commands()
        else:
            cmd_list = cmd_list + [NewCharacter]
        return cmd_list

    def __str__(self):
        return self.username


class UserUtils:
    @staticmethod
    def print_all(discord_users):
        print(" ".join([str(x) for x in discord_users]))

    @staticmethod
    def get_user_by_username(username, discord_users):
        for user in discord_users:
            if user.username == username:
                return user
        return None

    @staticmethod
    def get_user_by_character_name(character_name, discord_users):
        return next((x for x in discord_users if x.current_character == character_name), None)

    @staticmethod
    def get_character_by_username(username, discord_users):
        for user in discord_users:
            if user.username == username:
                return user.current_character
        return None


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
