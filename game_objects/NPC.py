from __future__ import annotations
from typing import Any, List

from game_objects.GameEntity import GameEntity


familiarity_levels = {
    "strangers": 0,
    "introduced": 1,
    "familiar": 2,
    "aquainted": 3,
    "close": 4
}

opinion_levels = {
    "hostile": -2,
    "unfriendly": -1,
    "indifferent": 0,
    "friendly": 1,
    "familial": 2
}


class NPC(GameEntity):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.current_room = None
        self.dialog_tree: dict = None
        self.relationship: dict = {}  # TODO relations will have an opinion and familiarity score, keyed from the player or npc name

    def get_relationship(self, other_name):
        try_get_relationship = self.relationship.get(other_name, None)
        if try_get_relationship is not None:
            return try_get_relationship
        else:
            return {
                "familiarity": 0,
                "opinion": 0
            }

    def set_relationship(self, other_name, relationship):
        self.relationship[other_name] = relationship


    def to_dict(self) -> dict:
        pass

    @classmethod
    def from_dict(cls, source_dict):
        to_return = NPC()
        to_return.__dict__.update(source_dict)
        return to_return
