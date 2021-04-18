from __future__ import annotations
from typing import Any, List

from game_objects.Commands.Command import Command
from game_objects.Commands.NoncombatCommands.LootCommand import LootCommand


class Fixture:
    # things you find in rooms like torch sconces, tables
    # they belong to the room and grant additional contextual actions to players in the room
    def __init__(self):
        self.template: Any = None

    def describe(self) -> str:
        return ""

    def get_commands(self) -> List[Command]:
        return []


class TreasureChest(Fixture):
    def __init__(self, lootable_items=None):
        import random
        from game_objects.Items.Weapon import Sword, Dagger, Spear, Mace, Axe, Torch
        from game_objects.Items.Shield import Shield
        from game_objects.Items.Armor import PlateArmor, ChainArmor, Gambeson
        from game_objects.Items.Item import Coins, DungeonMap
        from game_objects.Items.Consumable import HealthPotion, StaminaPotion
        from game_objects.LootTable import LootTable
        super().__init__()
        self.name = "Chest"
        self.items = LootTable(lootable_items or [
            (Coins(count=random.randint(0, 50)), .85),
            (HealthPotion(),                     .60),
            (DungeonMap(),                       .05),
            (StaminaPotion(),                    .30),
            (Shield(),                           .15),
            (Torch(),                            .05),
            (Dagger(),                           .05),
            (Axe(),                              .05),
            (Sword(),                            .05),
            (Mace(),                             .05),
            (Spear(),                            .05),
            (PlateArmor(),                       .05),
            (ChainArmor(),                       .05),
            (Gambeson(),                         .05)
        ]).roll_drops()

    def describe(self) -> str:
        if len(self.items) > 0:
            return "An old wooden treasure chest sits on the floor."
        else:
            return "An empty wooden treasure chest sits on the floor."

    def get_commands(self) -> List[Command]:
        return super().get_commands() + [LootCommand()]
