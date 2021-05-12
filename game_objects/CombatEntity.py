from typing import Optional


class CombatEntity:
    def __init__(self):
        super().__init__()
        from utils.CombatHelpers import assign_damage
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
        self.assign_damage = assign_damage
        self.base_actions = 2

    def add_status(self, game, status):
        self.status_effects.append(status)
        status.attach_triggers(game)
        status.on_attach(game)

    @property
    def display_health(self) -> str:
        return str(round(self.health, 1))

    @property
    def display_stamina(self) -> str:
        return str(round(self.stamina, 1))

    @property
    def display_mana(self) -> str:
        return str(round(self.mana, 1))

    @property
    def actions(self) -> int:
        to_return = self.base_actions
        for status in self.status_effects:
            to_return = to_return + status.actions
        return to_return

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
