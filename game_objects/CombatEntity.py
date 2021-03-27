from typing import Optional


class CombatEntity:
    def __init__(self):
        from game_objects.Room import Room
        self.health: int = 0
        self.max_health: int = 0
        self.stamina: int = 0
        self.max_stamina: int = 0
        self.mana: int = 0
        self.max_mana: int = 0
        self.current_room: Optional[Room] = None
        self.dead: bool = False

    @property
    def combat_name(self) -> str:
        raise Exception("Not Implemented")

    @property
    def resistances(self) -> dict:
        raise Exception("Not Implemented")

    @property
    def initiative(self) -> int:
        raise Exception("Not Implemented")