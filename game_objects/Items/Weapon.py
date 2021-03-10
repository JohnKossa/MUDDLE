from game_objects.Items.Equipment import Equipment
from game_objects.Combat import AttackAction


class Weapon(Equipment):
    def __init__(self):
        super().__init__()
        self.slot = "Hand"
        self.default_attack = None

    def get_commands(self):
        # will add "attack" command
        return super().get_commands() + []


class Sword(Weapon):
    def __init__(self):
        super().__init__()
        self.attacks = [
            AttackAction(name="slash", hit_bonus=2, dmg_type="slash", dmg_roll=(2, 6), dmg_bonus=1),
            AttackAction(name="stab", hit_bonus=1, dmg_type="pierce", dmg_roll=(1, 10), dmg_bonus=1),
            AttackAction(name="pommelstrike", hit_bonus=0, dmg_type="bludgeon", dmg_roll=(1, 6), dmg_bonus=0)
        ]
        self.default_attack = "slash"

    def get_commands(self):
        # will add slash, and stab commands
        return super().get_commands() + []
