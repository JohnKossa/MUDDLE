from __future__ import annotations
from game_objects.Character.Character import Character


class CharacterUtils:
    @staticmethod
    def print_all(player_list: list[Character]) -> None:
        print(" ".join([str(x) for x in player_list]))
