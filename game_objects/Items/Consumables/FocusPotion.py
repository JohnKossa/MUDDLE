from typing import Any, Optional

from Game import Game
from game_objects.Character.Character import Character
from game_objects.Items.Consumables.Consumable import Consumable
from game_objects.StatusEffect import StatusEffect
from utils.TriggerFunc import TriggerFunc


class FocusPotion(Consumable):
    def __init__(self):
        super().__init__()
        self.name = "FocusPotion"
        self.max_stack_size = 5

    def to_dict(self, full_depth=True) -> dict:
        to_return = super().to_dict()
        to_return.update({
            "constructor": self.__class__.__name__
        })
        return to_return

    @classmethod
    def from_dict(cls, source_dict):
        to_return = FocusPotion()
        to_return.__dict__.update(source_dict)
        return to_return

    def use_effect(self, game: Game, source_player: Character, params: list[Any]) -> None:
        game.discord_connection.send_game_chat_sync(f"{source_player.combat_name} drinks a focus potion. Hit chance increased.")
        status = FocusPotionStatus(source_player)
        source_player.add_status(game, status)


class FocusPotionStatus(StatusEffect):
    def __init__(self, parent, strength: Optional[int] = None, duration: Optional[int] = None):
        super().__init__(parent)
        from utils.Constanats import Triggers
        self.hit_bonus = 2 if strength is None else strength
        self.data = {
            "remaining_turns": 5 if duration is None else duration
        }
        self.triggers = {
            Triggers.BeforeEntityCombat: TriggerFunc(self.decrement_on_turn_start, self.parent),
            Triggers.LeaveRoom: TriggerFunc(self.detach_on_leave_room, self.parent)
        }

    def decrement_on_turn_start(self, source_player: Optional[Character] = None, game: Optional[Game] = None, **kwargs):
        if source_player == self.parent:
            self.data["remaining_turns"] = self.data["remaining_turns"] - 1
            if self.data["remaining_turns"] <= 0:
                game.discord_connection.send_game_chat_sync("You feel the effects of the focus potion begin to fade.", [source_player.discord_user])
                source_player.status_effects.remove(self)
                self.parent = None
                self.detach_triggers(game)

    def detach_on_leave_room(self, source_player: Optional[Character] = None, game: Optional[Game] = None, **kwargs):
        if source_player == self.parent:
            game.discord_connection.send_game_chat_sync("You feel the effects of the focus potion begin to fade.",
                                                   [source_player.discord_user])
            source_player.status_effects.remove(self)
            self.parent = None
            self.detach_triggers(game)