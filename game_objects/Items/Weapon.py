from game_objects.Items.Equipment import Equipment


class Weapon(Equipment):
    def __init__(self):
        super().__init__()
        self.slot = "Hand"

    def get_commands(self):
        # will add "attack" command
        return super().get_commands() + []


class Sword(Weapon):
    def __init__(self):
        super().__init__()
        self.default_attack = "slash"
        self.hit_bonus = {
            "slash": 0,
            "stab": 0
        }
        self.damage_bonus = {
            "slash": 0,
            "stab": 0
        }

    def get_commands(self):
        # will add slash, and stab commands
        return super().get_commands() + []