from __future__ import annotations
from typing import Any, List, Optional

import Game
from game_objects import Character
from game_objects.Commands.Command import Command


class Item:
    def __init__(self):
        self.quantity: int = 1
        self.max_stack_size: int = 1
        self.weight: int = 0
        self.name: str = "Item"
        self.template: Any = None

    @classmethod
    def from_template(cls, template_string) -> Item:
        # TODO fill out
        import json
        return Item()

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

    def use_effect(self, game: Game, source_player: Character, target_player: Character) -> None:
        # describes what happens when a player does !use with the item
        pass

    def get_commands(self) -> List[Command]:
        # will add the use and drop commands
        return []
