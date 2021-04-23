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
        self.reputations: dict = {}  # TODO relations will have an opinion and familiarity score, keyed from the player or npc name

    def to_dict(self) -> dict:
        pass

    @classmethod
    def from_dict(cls, source_dict):
        pass
