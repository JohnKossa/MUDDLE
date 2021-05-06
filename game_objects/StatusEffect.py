from __future__ import annotations

import Game
from game_objects.CombatEntity import CombatEntity


class StatusEffect(object):
    def __init__(self, parent: CombatEntity):
        self.hit_resistances = {}
        self.dmg_resistances = {}
        self.hit_bonus = 0
        self.dmg_bonus = 0
        self.triggers = {}
        self.data = {}
        self.actions = 0
        self.parent: CombatEntity = parent

    def attach_triggers(self, game: Game) -> None:
        for k, v, in self.triggers.items():
            game.on(k, v)

    def detach_triggers(self, game: Game) -> None:
        for k, v, in self.triggers.items():
            game.off(k, v)

