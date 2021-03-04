class Player:
    def __init__(self):
        self.name = None
        self.current_room = None
        self.zone = "Labrynth"
        self.skills = None
        self.inventory = None
        self.discord_user = None

    def get_commands(self):
        to_return = []
        if self.current_room is not None:
            to_return = to_return + self.current_room.get_commands()
        if self.skills is not None:
            to_return = to_return + self.skills.get_commands()
        if self.inventory is not None:
            to_return = to_return + self.inventory.get_commands()
        return to_return

    def __str__(self):
        return self.discord_user.username+" as "+("Unnamed Player" if self.name is None else self.name)


class PlayerInventory:
    def __init__(self):
        pass


class PlayerSkills:
    def __init__(self):
        pass


class PlayerUtils:
    @staticmethod
    def print_all(player_list):
        print(" ".join([str(x) for x in player_list]))
