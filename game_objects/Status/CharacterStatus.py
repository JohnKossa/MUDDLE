from __future__ import annotations

import Game


class CharacterStatus(object):
    def __init__(self, parent):
        self.hit_resistances = {}
        self.dmg_resistances = {}
        self.hit_bonus = 0
        self.dmg_bonus = 0
        self.triggers = {}
        self.data = {}
        self.character = parent

    def attach_triggers(self, game: Game):
        for k, v, in self.triggers.items():
            game.on(k, v)

    def detach_triggers(self, game: Game):
        for k, v, in self.triggers.items():
            game.off(k, v)

