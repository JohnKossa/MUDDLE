from __future__ import annotations
from typing import Optional

from Game import Game
from game_objects.CombatEntity import CombatEntity
from game_objects.StatusEffect import StatusEffect
from utils.Constanats import DamageTypes
from utils.TriggerFunc import TriggerFunc


class Soaked(StatusEffect):
    #  TODO: have this status remove the on fire status when applied
    def __init__(self, parent, turns=3):
        super().__init__(parent)
        from utils.Constanats import Triggers
        self.hit_resistances = {
            DamageTypes.Ice: -2,
            DamageTypes.Fire: 3,
            DamageTypes.Electricity: -10
        }
        self.dmg_resistances = {
            DamageTypes.Ice: -3,
            DamageTypes.Fire: 2,
            DamageTypes.Electricity: -5
        }
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
            game.discord_connection.send_game_chat_sync(f"{source_entity.combat_name} appears to have dried out.")

    def remove_on_leave_room(self, source_entity: Optional[CombatEntity] = None, game: Optional[Game] = None, **kwargs) -> None:
        if source_entity != self.parent:
            return
        self.parent.status_effects.remove(self)
        self.parent = None
        self.detach_triggers(game)
