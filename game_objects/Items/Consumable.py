from __future__ import annotations
from typing import Any, List
import Game
from game_objects.Character.Character import Character
from game_objects.Items.Item import Item


class Consumable(Item):
    def __init__(self):
        super().__init__()

    def use_effect(self, game: Game, source_player: Character, params: List[Any]) -> None:
        # describes what happens when a player does !use with the item
        pass


class HealthPotion(Consumable):
    def __init__(self):
        super().__init__()
        self.name = "HealthPotion"

    def to_dict(self, full_depth=True):
        to_return = super().to_dict()
        to_return.update({
            "constructor": self.__class__.__name__
        })
        return to_return

    def use_effect(self, game: Game, source_player: Character, params: List[Any]) -> None:
        from utils.Dice import roll
        raw_roll = roll(5, 6, source_player.luck)
        previous_health = source_player.health
        source_player.health = min(raw_roll+source_player.health, source_player.max_health)
        restored_amt = source_player.health - previous_health
        game.discord_connection.send_game_chat_sync(f"Restored {restored_amt} health.", [source_player.discord_user])


class ManaPotion(Consumable):
    def __init__(self):
        super().__init__()
        self.name = "ManaPotion"


class StaminaPotion(Consumable):
    def __init__(self):
        super().__init__()
        self.name = "Stamina Potion"

    def to_dict(self, full_depth=True):
        to_return = super().to_dict()
        to_return.update({
            "constructor": self.__class__.__name__
        })
        return to_return

    def use_effect(self, game: Game, source_player: Character, params: List[Any]) -> None:
        from utils.Dice import roll
        raw_roll = roll(5, 6, source_player.luck)
        previous_stamina = source_player.stamina
        source_player.stamina = min(raw_roll + source_player.stamina, source_player.max_stamina)
        restored_amt = source_player.stamina - previous_stamina
        game.discord_connection.send_game_char_sync(f"Restored {restored_amt} stamina.", [source_player.discord_user])
