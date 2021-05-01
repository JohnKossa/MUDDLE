from __future__ import annotations
from typing import Optional

from Game import Game
from game_objects.CombatEntity import CombatEntity
from game_objects.StatusEffect import StatusEffect
from utils.TriggerFunc import TriggerFunc


class OnFireStatus(StatusEffect):
    def __init__(self, parent):
        super().__init__(parent)
        self.hit_resistances = {}
        self.dmg_resistances = {}
        self.data = {
            "level": 1
        }
        self.triggers = {
            "before_player_combat": TriggerFunc(self.tick, self.parent),
            "leave_room": TriggerFunc(self.tick, self.parent)
        }

    def tick(self, source_entity: Optional[CombatEntity] = None, game: Optional[Game] = None, **kwargs) -> None:
        if source_entity != self.parent:
            return
        from utils.Dice import roll
        from utils.CombatHelpers import assign_damage
        resistances = source_entity.resistances
        fire_dmg_res = resistances["dmg"].get("fire", 0)
        fire_hit_res = resistances["hit"].get("fire", 0)
        dmg_roll = roll(self.data["level"], 6, fire_dmg_res)
        game.discord_connection.send_game_chat_sync(f"The fire on {source_entity.combat_name} rages. " + assign_damage(game, None, source_entity, dmg_roll))
        extinguish_roll = roll(1, 20, source_entity.luck + fire_hit_res)
        #  1, 2, 3, 4, 5 -> fire grows
        #  16, 17, 18, 19, 20 -> fire shrinks
        if extinguish_roll <= 5:
            self.data["level"] = self.data["level"] + 1
            game.discord_connection.send_game_chat_sync(f"The fire on {source_entity} grows even stronger.")
        elif extinguish_roll > 15:
            self.data["level"] = self.data["level"] - 1
            if self.data["level"] <= 0:
                self.parent.status_effects.remove(self)
                self.parent = None
                self.detach_triggers(game)
                game.discord_connection.send_game_chat_sync(f"The fire on {source_entity} goes out.")
            else:
                game.discord_connection.send_game_chat_sync(f"The fire on {source_entity} appears to shrink.")

        self.hit_resistances["fire"] = fire_hit_res + self.data["level"]
