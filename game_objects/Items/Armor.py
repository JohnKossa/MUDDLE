from game_objects.Items.Equipment import Equipment


class Armor(Equipment):
    def __init__(self):
        super().__init__()
        self.slot = "Body"
        # resistances bestowed to user when equipped. assumed to be 0 if not specified
        self.damage_resistances = {}
        self.hit_resistances = {}

    def get_commands(self):
        return super().get_commands() + []


class PlateArmor(Armor):
    def __init__(self):
        super().__init__()
        # resistances bestowed to user when equipped. assumed to be 0 if not specified
        self.name = "IronPlate"
        self.damage_resistances = {
            "slash": 2,
            "stab": 0,
            "bludgeon": 1,
            "electricity": -5
        }
        self.hit_resistances = {
            "slash": 3,
            "stab": 2,
            "bludgeon": 0,
            "electricity": -1
        }

    def get_commands(self):
        return super().get_commands() + []


class ChainArmor(Armor):
    def __init__(self):
        super().__init__()
        # resistances bestowed to user when equipped. assumed to be 0 if not specified
        self.name = "IronChainmail"
        self.damage_resistances = {
            "slash": 2,
            "stab": 1,
            "bludgeon": 2,
            "electricity": -3
        }
        self.hit_resistances = {
            "slash": 2,
            "stab": 1,
            "bludgeon": 0,
            "electricity": -1
        }

    def get_commands(self):
        return super().get_commands() + []
