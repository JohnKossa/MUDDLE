class Character:
    def __init__(self):
        self.name = None
        self.current_room = None
        self.zone = "Labrynth"
        self.skills = None
        self.inventory = PlayerInventory()
        self.discord_user = None
        self.max_health = 100
        self.health = 100
        self.max_stamina = 100
        self.stamina = 100
        self.max_mana = 100
        self.mana = 100

    def get_commands(self):
        # TODO add a character sheet command
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
        self.equipment = {
            "head": None,
            "body": None,
            "left_hand": None,
            "right_hand": None
        }
        self.bag = {}

    def get_commands(self):
        from game_objects.Command import Drop
        to_return = []
        if self.bag.keys():
            to_return = to_return + [Drop]
        return to_return


class PlayerSkills:
    def __init__(self):
        pass


class PlayerUtils:
    @staticmethod
    def print_all(player_list):
        print(" ".join([str(x) for x in player_list]))
