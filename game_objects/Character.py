import names

from utils.Dice import roll


class Character:
    def __init__(self, name=None):
        if name is None:
            self.name = names.get_full_name(gender='male')
        else:
            self.name = name
        self.current_room = None
        self.zone = "Labrynth"
        self.skills = CharacterSkills()
        self.inventory = CharacterInventory()
        self.discord_user = None
        self.max_health = 100
        self.health = 100
        self.max_stamina = 100
        self.stamina = 100
        self.max_mana = 100
        self.mana = 100
        self.actions = 2

    @property
    def initiative(self):
        return roll(1, 20, advantage=1)

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


class CharacterInventory:
    def __init__(self):
        self.equipment = {
            "head": None,
            "body": None,
            "left_hand": None,
            "right_hand": None,
            "belt": None
        }
        self.bag = {}

    def get_commands(self):
        from game_objects.Command import Drop
        to_return = []
        if self.bag.keys():
            to_return = to_return + [Drop]
        for slot in self.equipment.keys():
            if self.equipment.get(slot, None) is not None:
                to_return = to_return + self.equipment.get[slot].get_commands()
        return to_return


class CharacterSkills:
    def __init__(self):
        pass

    def get_commands(self):
        return []


class CharacterUtils:
    @staticmethod
    def print_all(player_list):
        print(" ".join([str(x) for x in player_list]))
