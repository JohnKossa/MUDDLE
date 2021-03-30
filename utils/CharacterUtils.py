from __future__ import annotations
from typing import List

from game_objects.Character.Character import Character


class CharacterUtils:
    @staticmethod
    def print_all(player_list: List[Character]) -> None:
        print(" ".join([str(x) for x in player_list]))
