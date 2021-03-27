from __future__ import annotations
from typing import Any, List

from game_objects.Commands.Command import Command
from game_objects.Commands.NoncombatCommands.LootCommand import LootCommand
from game_objects.Items.Item import Coins
from game_objects.LootTable import LootTable


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
        super().__init__()
        self.name = "Chest"
        self.items = LootTable(lootable_items or [
            (Coins(count=random.randint(0, 50)), .50),
            (Shield(),                           .10),
            (Torch(),                            .01),
            (Dagger(),                           .01),
            (Axe(),                              .01),
            (Sword(),                            .01),
            (Mace(),                             .01),
            (Spear(),                            .01),
            (PlateArmor(),                       .01),
            (ChainArmor(),                       .01),
            (Gambeson(),                         .01)
        ]).roll_drops()

    def describe(self) -> str:
        return "An old wooden treasure chest sits on the floor."

    def get_commands(self) -> List[Command]:
        return super().get_commands() + [LootCommand()]
