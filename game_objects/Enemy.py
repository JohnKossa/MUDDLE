import random
from game_objects.Combat import AttackAction
from utils.Dice import roll
from utils.CombatHelpers import sum_resistances


class Enemy:
    def __init__(self):
        self.current_room = None
        self.name = None
        self.description = None
        self.max_health = 50
        self.health = 50
        self.actions = 2
        self.dead = False
        self.natural_armor = {
            "hit": {},
            "dmg": {}
        }
        self.armor_bonus = {
            "hit": {},
            "dmg": {}
        }
        self.possible_actions = [
            (1, AttackAction(name="punch", hit_bonus=0, dmg_type="bludgeon", dmg_roll=(1, 6), dmg_bonus=0))
        ]

    @property
    def resistances(self):
        return {
            "hit": sum_resistances(self.natural_armor["hit"], self.armor_bonus["hit"]),
            "dmg": sum_resistances(self.natural_armor["dmg"], self.armor_bonus["dmg"])
        }

    @property
    def initiative(self):
        return roll(1, 20)

    def get_action(self):
        weighted_choices = random.choices([x[1] for x in self.possible_actions], weights=[x[0] for x in self.possible_actions], k=1)
        return weighted_choices[0] if weighted_choices else None
