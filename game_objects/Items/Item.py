from __future__ import annotations
from typing import Any, Optional

from game_objects.GameEntity import GameEntity


class Item(GameEntity):
    from game_objects import Character

    def __init__(self, **kwargs):
        super().__init__()
        self.quantity: int = 1
        self.max_stack_size: int = 1
        self.weight: int = 0
        self._basevalue: int = 0
        self.name: str = "Item"
        self.aliases:  list[str] = []
        self.traits:  list[str] = []
        self.template: Any = None
        self.quality: int = kwargs.get("quality", 50)
        self._condition: int = min(kwargs.get("condition", 100), self.quality)

    @property
    def value(self):
        if self.condition == 100:
            multiplier: float = 4.0
        elif self.condition > 90:
            multiplier: float = 3.0 + (self.condition - 90)/10.0
        else:
            multiplier: float = self.condition/50.0
        return int(self._basevalue * multiplier)


    @property
    def condition(self):
        return self._condition

    @condition.setter
    def condition(self, val):
        self._condition = min(self._condition, self.quality)

    def to_dict(self, full_depth=True) -> dict:
        return {
            "constructor": self.__class__.__name__,
            "quantity": self.quantity,
            "max_stack_size": self.max_stack_size,
            "weight": self.weight,
            "quality": self.quality,
            "_condition": self.condition,
            "name": self.name,
            "aliases": self.aliases,
            "traits": self.traits,
            "_basevalue": self._basevalue
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
        if self.quality != other.quality:
            return False
        if self.condition != other.condition:
            return False
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

    def use_effect(self, game: 'Game', source_player: Character, params:  list[Any]) -> None:
        # describes what happens when a player does !use with the item
        raise Exception(f"Use effect not implemented for {self.name}")

    def get_commands(self, game) ->  list['Command']:
        return []


class Coins(Item):
    def __init__(self, count=None):
        import random
        super().__init__()
        self.quantity: int = random.randrange(2, 9) if count is None else count
        self.max_stack_size: int = 1000000000
        self.weight = .03393
        self._basevalue = 1
        self.name: str = "GoldCoin"
        self.traits = self.traits + ["metallic", "currency", "tiny"]
        self.template: Any = None

    def describe(self) -> str:
        # TODO lookup item from template
        return "a disheveled pile of gold coins"


class DungeonMap(Item):
    def __init__(self):
        super().__init__()
        self.name: str = "DungeonMap"
        self.weight = .00045
