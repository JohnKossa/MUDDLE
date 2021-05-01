from typing import Optional


class CombatEntity:
    def __init__(self):
        super().__init__()
        from game_objects.Room import Room
        self.health: int = 0
        self.max_health: int = 0
        self.stamina: int = 0
        self.max_stamina: int = 0
        self.mana: int = 0
        self.max_mana: int = 0
        self.current_room: Optional[Room] = None
        self.dead: bool = False
        self.status_effects = []
        self.luck: int = 0

    @property
    def combat_name(self) -> str:
        raise Exception("Not Implemented")

    @property
    def resistances(self) -> dict:
        raise Exception("Not Implemented")

    @property
    def initiative(self) -> int:
        raise Exception("Not Implemented")

    @property
    def hit_bonus(self) -> int:
        raise Exception("Not Implemented")

    @property
    def dmg_bonus(self) -> int:
        raise Exception("Not Implemented")
