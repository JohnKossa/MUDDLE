from typing import List

from game_objects.Items.Item import Item
from utils.Dice import get_random


class LootTable:
    def __init__(self, items):
        self.items = items if items else []

    def add_item(self, item, drop_rate):
        self.items.append((item, drop_rate))

    def remove_item(self, item):
        self.items.remove(item)

    def roll_drops(self, luck=0) -> List[Item]:
        to_return = []
        for (item, chance) in self.items:
            if get_random(luck=luck) < chance:
                to_return.append(item)
        return to_return
