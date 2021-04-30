from __future__ import annotations
from typing import Any, List, Optional

from Game import Game
from game_objects.Character.Character import Character
from game_objects.Status.CharacterStatus import CharacterStatus
from utils.TriggerFunc import TriggerFunc


class RagePotionStatus(CharacterStatus):
    def __init__(self, parent):
        super().__init__(parent)
        self.dmg_bonus = 2
        self.data = {
            "remaining_turns": 5
        }
        self.triggers = {
            "before_player_combat": TriggerFunc(self.decrement_on_turn_start, self.character),
            "leave_room": TriggerFunc(self.detach_on_leave_room, self.character)
        }

    def decrement_on_turn_start(self, source_player: Optional[Character] = None, game: Optional[Game] = None, **kwargs):
        if source_player == self.character:
            self.data["remaining_turns"] = self.data["remaining_turns"] - 1
            if self.data["remaining_turns"] <= 0:
                game.discord_connection.send_game_chat("The effects of the rage potion begin to fade.", [source_player.discord_user])
                source_player.status_effects.remove(self)
                self.character = None
                self.detach_triggers(game)

    def detach_on_leave_room(self, source_player: Optional[Character] = None, game: Optional[Game] = None, **kwargs):
        if source_player == self.character:
            source_player.status_effects.remove(self)
            self.character = None
            self.detach_triggers(game)
