from __future__ import annotations
from typing import Optional
import random
import Game
from game_objects.AttackAction import AttackAction
from game_objects.CombatEntity import CombatEntity
from game_objects.GameEntity import GameEntity
from utils.Constanats import DamageTypes
from utils.Dice import roll
from utils.CombatHelpers import sum_resistances


class Enemy(CombatEntity, GameEntity):
    from game_objects.Commands.CombatCommands.AttackCommand import AttackCommand

    def __init__(self):
        super().__init__()
        from game_objects.Room import Room
        from game_objects.LootTable import LootTable
        self.current_room: Optional[Room] = None
        self.name: str = None
        self.disambiguation_num: int = 0
        self.description: str = None
        self.max_health: int = 50
        self.health: int = 50
        self.traits = []
        self.natural_armor: dict = {
            "hit": {},
            "dmg": {}
        }
        self.armor_bonus: dict = {
            "hit": {},
            "dmg": {}
        }
        self.possible_attacks: list[(int, AttackAction)] = [
            (1, AttackAction(name="punch", hit_bonus=0, dmg_type=DamageTypes.Bludgeon, dmg_roll=(1, 4), dmg_bonus=0))
        ]
        from game_objects.Items.Weapon import Sword, Dagger, Spear, Mace, Axe, Torch
        from game_objects.Items.Item import Coins
        self.loot_table = LootTable([
            (Coins(count=random.randint(1, 10)), .30),
            (Torch(),                            .10),
            (Dagger(),                           .10),
            (Axe(),                              .08),
            (Sword(),                            .05),
            (Mace(),                             .03),
            (Spear(),                            .03)
        ])
        self.drops = self.loot_table.roll_drops()

    @property
    def resistances(self) -> dict:  # TODO create a type for this
        to_return = {
            "hit": sum_resistances(self.natural_armor["hit"], self.armor_bonus["hit"]),
            "dmg": sum_resistances(self.natural_armor["dmg"], self.armor_bonus["dmg"])
        }
        for status in self.status_effects:
            to_return["hit"] = sum_resistances(to_return["hit"], status.hit_resistances)
            to_return["dmg"] = sum_resistances(to_return["dmg"], status.dmg_resistances)
        return to_return

    @property
    def hit_bonus(self) -> int:
        to_return = 0
        for status in self.status_effects:
            to_return = to_return + status.hit_bonus
        return to_return

    @property
    def dmg_bonus(self) -> int:
        to_return = 0
        for status in self.status_effects:
            to_return = to_return + status.dmg_bonus
        return to_return

    @property
    def initiative(self) -> int:
        return roll(1, 20)

    @property
    def combat_name(self) -> str:
        if self.disambiguation_num == 0:
            return self.name
        return f"{self.name}{self.disambiguation_num}"

    def cleanup(self, game: Game) -> None:
        game.enemies_dict.pop(self.guid)
        if self.current_room.combat is not None:
            if self in self.current_room.combat.enemies:
                self.current_room.combat.enemies.remove(self)

    def get_action(self, **kwargs) -> AttackCommand:
        from game_objects.Commands.CombatCommands.AttackCommand import AttackCommand
        weighted_choices = random.choices([x[1] for x in self.possible_attacks], weights=[x[0] for x in self.possible_attacks], k=1)
        attack_action = weighted_choices[0] if weighted_choices else None
        return AttackCommand(attack_action)


class Goblin(Enemy):
    def __init__(self):
        super().__init__()
        from game_objects.LootTable import LootTable
        self.name = "Goblin"
        self.health = 25
        self.max_health = 25
        self.traits = self.traits + ["goblin", "humanoid"]
        self.possible_attacks: list[(int, AttackAction)] = [
            (1, AttackAction(name="punch", hit_bonus=0, dmg_type=DamageTypes.Bludgeon, dmg_roll=(1, 4), dmg_bonus=0)),
            (3, AttackAction(name="stab", hit_bonus=1, dmg_type=DamageTypes.Pierce, dmg_roll=(1, 10), dmg_bonus=0))
        ]
        from game_objects.Items.Weapon import Sword, Dagger, Spear, Mace, Axe, Torch
        from game_objects.Items.Item import Coins
        from game_objects.Items.Consumables.HealthPotion import HealthPotion
        from game_objects.Items.Consumables.StaminaPotion import StaminaPotion
        self.loot_table = LootTable([
            (Coins(count=random.randint(1, 10)), .30),
            (HealthPotion(quality=random.randint(1, 70), condition=100),  .20),
            (StaminaPotion(quality=random.randint(1, 70), condition=100), .10),
            (Torch(quality=random.randint(1, 70), condition=100),         .10),
            (Dagger(quality=random.randint(1, 70), condition=100),        .10),
            (Axe(quality=random.randint(1, 70), condition=100),           .08),
            (Sword(quality=random.randint(1, 70), condition=100),         .05),
            (Mace(quality=random.randint(1, 70), condition=100),          .03),
            (Spear(quality=random.randint(1, 70), condition=100),         .03)
        ])
        self.drops = self.loot_table.roll_drops()


class Kobold(Enemy):
    def __init__(self):
        super().__init__()
        from game_objects.LootTable import LootTable
        self.name = "Kobold"
        self.health = 15
        self.max_health = 15
        self.traits = self.traits + ["kobold", "humanoid", "draconic"]
        self.possible_attacks: list[(int, AttackAction)] = [
            (1, AttackAction(name="punch", hit_bonus=0, dmg_type=DamageTypes.Bludgeon, dmg_roll=(1, 4), dmg_bonus=0)),
            (1, AttackAction(name="slash", hit_bonus=1, dmg_type=DamageTypes.Slash, dmg_roll=(2, 4), dmg_bonus=0)),
            (1, AttackAction(name="stab", hit_bonus=3, dmg_type=DamageTypes.Pierce, dmg_roll=(3, 4), dmg_bonus=0))
        ]
        from game_objects.Items.Weapon import Sword, Dagger, Spear, Mace, Axe, Torch
        from game_objects.Items.Item import Coins
        from game_objects.Items.Consumables.HealthPotion import HealthPotion
        from game_objects.Items.Consumables.StaminaPotion import StaminaPotion
        self.loot_table = LootTable([
            (Coins(count=random.randint(1, 10)), .50),
            (Dagger(quality=random.randint(1, 70), condition=100),                           .50),
            (HealthPotion(quality=random.randint(1, 70), condition=100),                     .20),
            (StaminaPotion(quality=random.randint(1, 70), condition=100),                    .10),
            (Torch(quality=random.randint(1, 70), condition=100),                            .10),
            (Axe(quality=random.randint(1, 70), condition=100),                              .03),
            (Sword(quality=random.randint(1, 70), condition=100),                            .03),
            (Mace(quality=random.randint(1, 70), condition=100),                             .03),
            (Spear(quality=random.randint(1, 70), condition=100),                            .03)
        ])
        self.drops = self.loot_table.roll_drops()


class Orc(Enemy):
    def __init__(self):
        from game_objects.Items.Armor import PlateArmor
        from game_objects.Items.Weapon import Sword, Spear, Mace, Axe
        from game_objects.LootTable import LootTable
        super().__init__()
        self.name = "Orc"
        self.health = 75
        self.max_health = 75
        self.traits = self.traits + ["orc", "humanoid"]
        self.possible_attacks: list[(int, AttackAction)] = [
            (1, AttackAction(name="punch", hit_bonus=0, dmg_type=DamageTypes.Bludgeon, dmg_roll=(1, 4), dmg_bonus=1)),
            (3, AttackAction(name="slash", hit_bonus=1, dmg_type=DamageTypes.Slash, dmg_roll=(1, 16), dmg_bonus=0))
        ]
        self.armor_bonus: dict = {
            "hit": {
                DamageTypes.Slash: 2,
                DamageTypes.Pierce: 1,
                DamageTypes.Electricity: -1
            },
            "dmg": {
                DamageTypes.Pierce: 2,
                DamageTypes.Bludgeon: 1,
                DamageTypes.Electricity: -5
            }
        }
        from game_objects.Items.Consumables.HealthPotion import HealthPotion
        from game_objects.Items.Consumables.StaminaPotion import StaminaPotion
        from game_objects.Items.Item import Coins
        self.loot_table = LootTable([
            (Coins(count=random.randint(1, 100)), .50),
            (HealthPotion(quality=random.randint(1, 70), condition=100),                      .50),
            (PlateArmor(quality=random.randint(20, 70), condition=100),                        .30),
            (StaminaPotion(quality=random.randint(1, 70), condition=100),                     .20),
            (Axe(quality=random.randint(20, 70), condition=100),                               .20),
            (Sword(quality=random.randint(20, 70), condition=100),                             .10),
            (Mace(quality=random.randint(20, 70), condition=100),                              .10),
            (Spear(quality=random.randint(20, 70), condition=100),                             .10)
        ])
        self.drops = self.loot_table.roll_drops()
