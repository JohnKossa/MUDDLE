import random
from game_objects.Combat import AttackAction


class Enemy:
    def __init__(self):
        self.room = None
        self.name = None
        self.description = None
        self.max_health = 50
        self.health = 50
        self.armor_bonus = {}
        self.actions = [
            (1, AttackAction(name="punch", hit_bonus=0, dmg_type="bludgeon", dmg_roll=(1, 6), dmg_bonus=0))
        ]

    def get_action(self):
        # TODO replace with weighted choice
        return random.choice(self.actions[1])
