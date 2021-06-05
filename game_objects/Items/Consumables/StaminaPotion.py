from __future__ import annotations
from typing import Any

import Game
from game_objects.Character.Character import Character
from game_objects.Items.Consumables.Consumable import Consumable


class StaminaPotion(Consumable):
    def __init__(self):
        super().__init__()
        self.name = "StaminaPotion"
        self.max_stack_size = 5

    def to_dict(self, full_depth=True) -> dict:
        to_return = super().to_dict()
        to_return.update({
            "constructor": self.__class__.__name__
        })
        return to_return

    @classmethod
    def from_dict(cls, source_dict) -> StaminaPotion:
        to_return = StaminaPotion()
        to_return.__dict__.update(source_dict)
        return to_return

    def use_effect(self, game: Game, source_player: Character, params: list[Any]) -> None:
        from utils.Dice import roll
        raw_roll = roll(5, 20, source_player.luck)
        previous_stamina = source_player.stamina
        source_player.stamina = min(raw_roll + source_player.stamina, source_player.max_stamina)
        restored_amt = source_player.stamina - previous_stamina
        game.discord_connection.send_game_chat_sync(f"Restored {restored_amt} stamina.", [source_player.discord_user])