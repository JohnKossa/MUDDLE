from typing import List


class CharacterSpells:
    from game_objects.Commands.Command import Command

    def __init__(self):
        self.known_spells = []

    def to_dict(self):
        return {}

    def get_commands(self, game) -> List[Command]:
        return []
