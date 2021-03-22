class AttackAction:
    def __init__(self, name: str = "attack", hit_bonus: int = 0, dmg_type: str = "bludgeon", dmg_roll: (int, int) = (1, 6), dmg_bonus: int = 0, action_cost: int = 1):
        self.name: str = name
        self.hit_bonus: int = hit_bonus
        self.dmg_type: str = dmg_type
        self.dmg_roll: (int, int) = dmg_roll
        self.dmg_bonus: int = dmg_bonus
        self.action_cost: int = action_cost