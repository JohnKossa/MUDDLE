from game_objects.Commands.Command import RebuildMaze, NewCharacter


class DiscordUser:
    def __init__(self, username=None, current_character=None, discord_obj=None):
        self.username = username
        self.current_character = current_character
        self.is_admin = True if username == "kg959#1350" else False
        self.discord_obj = discord_obj

    def get_commands(self):
        from game_objects.Commands.Command import ShowMap, ShowAliases, ListCommands, ShowHelp
        cmd_list = [ListCommands(), ShowAliases(), ShowMap(), ShowHelp()]
        if self.current_character is not None:
            cmd_list = cmd_list + self.current_character.get_commands()
        else:
            cmd_list = cmd_list + [NewCharacter()]
        if self.is_admin:
            cmd_list = cmd_list + [RebuildMaze()]
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


