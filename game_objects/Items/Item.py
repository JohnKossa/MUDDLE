from __future__ import annotations
from typing import Any, List, Optional

import Game
from game_objects import Character
from game_objects.Commands.Command import Command
from game_objects.GameEntity import GameEntity


class Item(GameEntity):
    def __init__(self):
        super().__init__()
        self.quantity: int = 1
        self.max_stack_size: int = 1
        self.weight: int = 0
        self.name: str = "Item"
        self.template: Any = None

    def to_dict(self, full_depth=True) -> dict:
        return {
            "constructor": self.__class__.__name__,
            "quantity": self.quantity,
            "max_stack_size": self.max_stack_size,
            "weight": self.weight,
            "name": self.name,
        }

    @classmethod
    def from_dict(cls, source_dict) -> Item:
        to_return = Item()
        to_return.__dict__.update(source_dict)
        return to_return

    def describe(self) -> str:
        # TODO lookup item from template
        if self.template is None:
            return f"a {self.name}"
        else:
            return "This needs to look up the description from the template"

    def able_to_join(self, other: Item) -> bool:
        if self.name != other.name:
            return False
        if self.quantity + other.quantity > self.max_stack_size:
            return False
        # TODO when we add durability, if durability doesn't match, return false
        # TODO when we add custom effects (magic), return false if either has one
        return True

    def take_count_from_stack(self, count: int) -> Optional[Item]:
        if count >= self.quantity:
            return self
        self.quantity = self.quantity - count
        new_item = Item()
        new_item.quantity = count
        new_item.max_stack_size = self.max_stack_size
        new_item.weight = self.weight
        new_item.name = self.name
        new_item.template = self.template
        return new_item

    def use_effect(self, game: Game, source_player: Character, params: List[Any]) -> None:
        # describes what happens when a player does !use with the item
        raise Exception(f"Use effect not implemented for {self.name}")

    def get_commands(self) -> List[Command]:
        return []


class Coins(Item):
    def __init__(self, count=None):
        import random
        super().__init__()
        self.quantity: int = random.randrange(2, 9) if count is None else count
        self.max_stack_size: int = 1000000000
        self.weight: int = 0
        self.name: str = "GoldCoin"
        self.template: Any = None

    def describe(self) -> str:
        # TODO lookup item from template
        return "a disheveled pile of gold coins"


class DungeonMap(Item):
    def __init__(self):
        super().__init__()
        self.name: str = "DungeonMap"
