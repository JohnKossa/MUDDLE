from __future__ import annotations
from typing import Optional

from Game import Game
from game_objects.CombatEntity import CombatEntity
from game_objects.StatusEffect import StatusEffect
from utils.TriggerFunc import TriggerFunc


class Soaked(StatusEffect):
    #  TODO: have this status remove the on fire status when applied
    def __init__(self, parent, turns=3):
        super().__init__(parent)
        self.hit_resistances = {
            "ice": -2,
            "fire": 3,
            "electricity": -10
        }
        self.dmg_resistances = {
            "ice": -3,
            "fire": 2,
            "electricity": -5
        }
        self.data = {
            "turns": turns
        }
        self.triggers = {
            "before_entity_combat": TriggerFunc(self.tick),
            "leave_room": TriggerFunc(self.remove_on_leave_room)
        }

    def tick(self, source_entity: Optional[CombatEntity] = None, game: Optional[Game] = None, **kwargs) -> None:
        if source_entity != self.parent:
            return
        self.data["turns"] = self.data["turns"] - 1
        if self.data["turns"] <= 0:
            self.parent.status_effects.remove(self)
            self.parent = None
            self.detach_triggers(game)
            game.discord_connection.send_game_chat_sync(f"{source_entity.combat_name} appears to have dried out.")

    def remove_on_leave_room(self, source_entity: Optional[CombatEntity] = None, game: Optional[Game] = None, **kwargs) -> None:
        if source_entity != self.parent:
            return
        self.parent.status_effects.remove(self)
        self.parent = None
        self.detach_triggers(game)
