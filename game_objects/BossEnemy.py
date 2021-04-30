from __future__ import annotations
import random
from typing import List
from game_objects.Enemy import Enemy


class BossEnemy(Enemy):
    def __init__(self):
        super().__init__()


class StoneGolem(BossEnemy):
    def __init__(self):
        from game_objects.AttackAction import AttackAction
        from game_objects.Items.Weapon import Sword, Dagger, Spear, Mace, Axe, Torch
        from game_objects.Items.Item import Coins, Item
        super().__init__()
        self.name: str = "Stone Golem"
        self.max_health = 150
        self.health = 150
        self.natural_armor = {
            "hit": {
                "slash": 3,
                "fire": 5,
                "pierce": 2,
                "bludgeon": 0
            },
            "dmg": {
                "slash": 1,
                "fire": 5,
                "pierce": 1,
                "bludgeon": -3,
                "ice": 1
            }
        }
        self.possible_attacks: List[(int, AttackAction)] = [
            (2, AttackAction(name="punch",
                             hit_bonus=1,
                             dmg_type="bludgeon",
                             dmg_roll=(2, 10),
                             dmg_bonus=0,
                             action_cost=1)),
            (1, AttackAction(name="smash",
                             hit_bonus=2,
                             dmg_type="bludgeon",
                             dmg_roll=(3, 20),
                             dmg_bonus=0,
                             action_cost=2))
        ]
        self.drops: List[Item] = [Coins(count=random.randint(100, 300))] + random.choices(
            [Sword(), Dagger(), Spear(), Mace(), Axe(), Torch()], k=4)


class StrawGolem(BossEnemy):
    def __init__(self):
        from game_objects.AttackAction import AttackAction
        from game_objects.Items.Weapon import Sword, Dagger, Spear, Mace, Axe, Torch
        from game_objects.Items.Item import Coins, Item
        super().__init__()
        self.name: str = "Straw Golem"
        self.max_health = 150
        self.health = 150
        self.natural_armor = {
            "hit": {
                "slash": -1,
                "fire": -5,
                "pierce": 1,
                "bludgeon": 2
            },
            "dmg": {
                "slash": -1,
                "fire": -5,
                "pierce": 1,
                "bludgeon": 3,
                "ice": 3
            }
        }
        self.possible_attacks: List[(int, AttackAction)] = [
            (2, AttackAction(name="punch",
                             hit_bonus=1,
                             dmg_type="bludgeon",
                             dmg_roll=(2, 10),
                             dmg_bonus=0,
                             action_cost=1)),
            (1, AttackAction(name="hay hook",
                             hit_bonus=2,
                             dmg_type="pierce",
                             dmg_roll=(3, 6),
                             dmg_bonus=1,
                             action_cost=1)),
            (1, AttackAction(name="smash",
                             hit_bonus=2,
                             dmg_type="bludgeon",
                             dmg_roll=(3, 20),
                             dmg_bonus=0,
                             action_cost=2))
        ]
        self.drops: List[Item] = [Coins(count=random.randint(100, 300))] + random.choices([Sword(), Dagger(), Spear(), Mace(), Axe(), Torch()], k=4)
