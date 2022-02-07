from __future__ import annotations
import random
from game_objects.Enemy import Enemy
from utils.Constanats import DamageTypes


class BossEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.traits = self.traits + ["boss"]


class StoneGolem(BossEnemy):
    def __init__(self):
        from game_objects.AttackAction import AttackAction
        from game_objects.Items.Weapon import Sword, Dagger, Spear, Mace, Axe, Torch, DuelistDagger, WerebatFang, \
            PerunsPike, CrudgelOfChione, RavensBeak
        from game_objects.Items.Item import Coins, Item
        super().__init__()
        self.name: str = "StoneGolem"
        self.max_health = 150
        self.health = 150
        self.traits = self.traits + ["construct", "stone"]
        self.natural_armor = {
            "hit": {
                DamageTypes.Slash: 3,
                DamageTypes.Fire: 5,
                DamageTypes.Pierce: 2,
                DamageTypes.Bludgeon: 0
            },
            "dmg": {
                DamageTypes.Slash: 1,
                DamageTypes.Fire: 5,
                DamageTypes.Pierce: 1,
                DamageTypes.Bludgeon: -3,
                DamageTypes.Ice: 1
            }
        }
        self.possible_attacks: list[(int, AttackAction)] = [
            (2, AttackAction(name="punch",
                             hit_bonus=1,
                             dmg_type=DamageTypes.Bludgeon,
                             dmg_roll=(2, 10),
                             dmg_bonus=0,
                             action_cost=1)),
            (1, AttackAction(name="smash",
                             hit_bonus=2,
                             dmg_type=DamageTypes.Bludgeon,
                             dmg_roll=(3, 20),
                             dmg_bonus=0,
                             action_cost=2))
        ]
        self.drops: list[Item] = [Coins(count=random.randint(100, 300))] + random.choices(
            [
                Sword(),
                Dagger(),
                Spear(),
                Mace(),
                Axe(),
                Torch()
            ], k=4) + random.choices([
                DuelistDagger(),
                WerebatFang(),
                PerunsPike(),
                CrudgelOfChione(),
                RavensBeak()
            ], k=1)


class StrawGolem(BossEnemy):
    def __init__(self):
        from game_objects.AttackAction import AttackAction
        from game_objects.Items.Weapon import Sword, Dagger, Spear, Mace, Axe, Torch, DuelistDagger, WerebatFang, \
            PerunsPike, CrudgelOfChione, RavensBeak
        from game_objects.Items.Item import Coins, Item
        super().__init__()
        self.name: str = "StrawGolem"
        self.max_health = 150
        self.health = 150
        self.traits = self.traits + ["construct"]
        self.natural_armor = {
            "hit": {
                DamageTypes.Slash: -1,
                DamageTypes.Fire: -5,
                DamageTypes.Pierce: 1,
                DamageTypes.Bludgeon: 2
            },
            "dmg": {
                DamageTypes.Slash: -1,
                DamageTypes.Fire: -5,
                DamageTypes.Pierce: 1,
                DamageTypes.Bludgeon: 3,
                DamageTypes.Ice: 3
            }
        }
        self.possible_attacks: list[(int, AttackAction)] = [
            (2, AttackAction(name="punch",
                             hit_bonus=1,
                             dmg_type=DamageTypes.Bludgeon,
                             dmg_roll=(2, 10),
                             dmg_bonus=0,
                             action_cost=1)),
            (1, AttackAction(name="hay hook",
                             hit_bonus=2,
                             dmg_type=DamageTypes.Pierce,
                             dmg_roll=(3, 6),
                             dmg_bonus=1,
                             action_cost=1)),
            (1, AttackAction(name="smash",
                             hit_bonus=2,
                             dmg_type=DamageTypes.Bludgeon,
                             dmg_roll=(3, 20),
                             dmg_bonus=0,
                             action_cost=2))
        ]
        self.drops: list[Item] = [Coins(count=random.randint(100, 300))] + random.choices([
            Sword(),
            Dagger(),
            Spear(),
            Mace(),
            Axe(),
            Torch()
        ], k=4) + random.choices([
            DuelistDagger(),
            WerebatFang(),
            PerunsPike(),
            CrudgelOfChione(),
            RavensBeak()
        ], k=1)
