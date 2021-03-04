class DiscordUser:
    def __init__(self):
        self.username = None
        self.current_character = None


class UserUtils:
    @staticmethod
    def get_user_by_character_name(character_name, discord_users):
        return next((x for x in discord_users if x.current_character == character_name), None)

    @staticmethod
    def get_character_by_username(username, discord_users):
        return next((x for x in discord_users if x.username == username), None)
