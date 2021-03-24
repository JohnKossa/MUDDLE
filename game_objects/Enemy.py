from __future__ import annotations
from typing import List, Optional
import random
from game_objects.CombatEntity import CombatEntity
from game_objects.AttackAction import AttackAction
from game_objects.LootTable import LootTable
from utils.Dice import roll
from utils.CombatHelpers import sum_resistances, assign_damage


class Enemy(CombatEntity):
    def __init__(self):
        super().__init__()
        from game_objects.Room import Room
        self.current_room: Optional[Room] = None
        self.name: str = None
        self.disambiguation_num: int = 0
        self.description: str = None
        self.max_health: int = 50
        self.health: int = 50
        self.actions: int = 2
        self.natural_armor: dict = {
            "hit": {},
            "dmg": {}
        }
        self.armor_bonus: dict = {
            "hit": {},
            "dmg": {}
        }
        self.possible_actions: List[(int, AttackAction)] = [
            (1, AttackAction(name="punch", hit_bonus=0, dmg_type="bludgeon", dmg_roll=(1, 6), dmg_bonus=0))
        ]
        self.assign_damage = assign_damage
        from game_objects.Items.Weapon import Sword, Dagger, Spear, Mace, Axe, Torch
        self.loot_table = LootTable([
            (Torch(),  .10),
            (Dagger(), .10),
            (Axe(),    .08),
            (Sword(),  .05),
            (Mace(),   .03),
            (Spear(),  .03)
        ])

    @property
    def resistances(self) -> dict:  # TODO create a type for this
        return {
            "hit": sum_resistances(self.natural_armor["hit"], self.armor_bonus["hit"]),
            "dmg": sum_resistances(self.natural_armor["dmg"], self.armor_bonus["dmg"])
        }

    @property
    def initiative(self) -> int:
        return roll(1, 20)

    @property
    def combat_name(self) -> str:
        if self.disambiguation_num == 0:
            return self.name
        return f"{self.name}{self.disambiguation_num}"

    def get_action(self) -> AttackAction:
        weighted_choices = random.choices([x[1] for x in self.possible_actions], weights=[x[0] for x in self.possible_actions], k=1)
        return weighted_choices[0] if weighted_choices else None
