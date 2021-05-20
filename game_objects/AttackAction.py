from __future__ import annotations

from utils.Constanats import DamageTypes


class AttackAction:
    def __init__(self, name: str = "attack", hit_bonus: int = 0, dmg_type: str = DamageTypes.Bludgeon, dmg_roll: (int, int) = (1, 6), dmg_bonus: int = 0, action_cost: int = 1):
        self.name: str = name
        self.hit_bonus: int = hit_bonus
        self.dmg_type: str = dmg_type
        self.dmg_roll: (int, int) = dmg_roll
        self.dmg_bonus: int = dmg_bonus
        self.action_cost: int = action_cost

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "hit_bonus": self.hit_bonus,
            "dmg_type": self.dmg_type,
            "dmg_roll": self.dmg_roll,
            "dmg_bonus": self.dmg_bonus,
            "action_cost": self.action_cost
        }

    @classmethod
    def from_dict(cls, source_dict) -> AttackAction:
        to_return = AttackAction()
        to_return.__dict__.update(source_dict)
        return to_return
