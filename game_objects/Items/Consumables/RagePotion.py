from typing import List, Any, Optional

from Game import Game
from game_objects.Character.Character import Character
from game_objects.Items.Consumables.Consumable import Consumable
from game_objects.Items.Consumables.StaminaPotion import StaminaPotion
from game_objects.Character.CharacterStatus import CharacterStatus
from utils.TriggerFunc import TriggerFunc


class RagePotion(Consumable):
    def __init__(self):
        super().__init__()
        self.name = "RagePotion"
        self.max_stack_size = 5

    def to_dict(self, full_depth=True) -> dict:
        to_return = super().to_dict()
        to_return.update({
            "constructor": self.__class__.__name__
        })
        return to_return

    @classmethod
    def from_dict(cls, source_dict):
        to_return = StaminaPotion()
        to_return.__dict__.update(source_dict)
        return to_return

    def use_effect(self, game: Game, source_player: Character, params: List[Any]) -> None:
        game.discord_connection.send_game_chat_sync(f"{source_player.combat_name} drinks a rage potion. Damage increased.")
        status = RagePotionStatus(source_player)
        status.attach_triggers(game)
        source_player.status_effects.append(status)


class RagePotionStatus(CharacterStatus):
    def __init__(self, parent, strength: Optional[int] = None, duration: Optional[int] = None):
        super().__init__(parent)
        self.dmg_bonus = 2 if strength is None else strength
        self.data = {
            "remaining_turns": 5 if duration is None else duration
        }
        self.triggers = {
            "before_player_combat": TriggerFunc(self.decrement_on_turn_start, self.character),
            "leave_room": TriggerFunc(self.detach_on_leave_room, self.character)
        }

    def decrement_on_turn_start(self, source_player: Optional[Character] = None, game: Optional[Game] = None, **kwargs):
        if source_player == self.character:
            self.data["remaining_turns"] = self.data["remaining_turns"] - 1
            if self.data["remaining_turns"] <= 0:
                game.discord_connection.send_game_chat("You feel the effects of the rage potion begin to fade.", [source_player.discord_user])
                source_player.status_effects.remove(self)
                self.character = None
                self.detach_triggers(game)

    def detach_on_leave_room(self, source_player: Optional[Character] = None, game: Optional[Game] = None, **kwargs):
        if source_player == self.character:
            game.discord_connection.send_game_chat("You feel the effects of the rage potion begin to fade.", [source_player.discord_user])
            source_player.status_effects.remove(self)
            self.character = None
            self.detach_triggers(game)