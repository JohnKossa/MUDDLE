from typing import List


class CharacterSkills:
    from game_objects.Commands.Command import Command

    def __init__(self):
        pass

    def to_dict(self):
        return {}

    @classmethod
    def from_dict(cls, source_dict):
        return CharacterSkills()

    def get_commands(self) -> List[Command]:
        return []