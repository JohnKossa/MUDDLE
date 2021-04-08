from __future__ import annotations
from typing import Any, List, Optional

from Game import Game
from game_objects.Character.Character import Character
from game_objects.Status.CharacterStatus import CharacterStatus
from utils.TriggerFunc import TriggerFunc


class DodgeStatus(CharacterStatus):
    def __init__(self, parent):
        super().__init__(parent)
        self.hit_resistances = {
            "bludgeon": 1,
            "pierce": 1,
            "slash": 1,
            "electricity": 1,
            "ice": 1,
            "fire": 1
        }
        self.triggers = {
            "before_player_combat": TriggerFunc(self.detach_on_turn_start, self.character),
            "leave_room": TriggerFunc(self.detach_on_turn_start, self.character)
        }

    def detach_on_turn_start(self, source_player: Optional[Character] = None, game: Optional[Game] = None, **kwargs):
        if source_player == self.character:
            source_player.status_effects.remove(self)
            self.character = None
            self.detach_triggers(game)
