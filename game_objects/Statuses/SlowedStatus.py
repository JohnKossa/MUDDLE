from __future__ import annotations
from typing import Optional

from Game import Game
from game_objects.CombatEntity import CombatEntity
from game_objects.StatusEffect import StatusEffect
from utils.TriggerFunc import TriggerFunc


class SlowedStatus(StatusEffect):
    # TODO if parent already has hasted status, this cancels it.
    def __init__(self, parent, turns=5):
        super().__init__(parent)
        from utils.Constanats import Triggers
        self.actions = -1
        self.data = {
            "turns": turns
        }
        self.triggers = {
            Triggers.BeforeEntityCombat: TriggerFunc(self.tick),
            Triggers.LeaveRoom: TriggerFunc(self.remove_on_leave_room)
        }

    def tick(self, source_entity: Optional[CombatEntity] = None, game: Optional[Game] = None, **kwargs) -> None:
        if source_entity != self.parent:
            return
        self.data["turns"] = self.data["turns"] - 1
        if self.data["turns"] <= 0:
            self.parent.status_effects.remove(self)
            self.parent = None
            self.detach_triggers(game)
            game.discord_connection.send_game_chat_sync(f"{source_entity.combat_name} appears to return to normal speed.")

    def remove_on_leave_room(self, source_entity: Optional[CombatEntity] = None, game: Optional[Game] = None, **kwargs) -> None:
        if source_entity != self.parent:
            return
        self.parent.status_effects.remove(self)
        self.parent = None
        self.detach_triggers(game)
