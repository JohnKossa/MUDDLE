from __future__ import annotations
from typing import Any, List

from Game import Game
from game_objects.Character import Character
from game_objects.Commands.CombatCommands.CombatCommand import CombatOnlyCommand
from utils.CombatHelpers import assign_damage as default_damage_assignment


class BlockCommand(CombatOnlyCommand):
    def __init__(self, aliases: List[str] = None):
        super().__init__()
        self.combat_action_cost: int = 1
        if aliases is not None:
            self.aliases: List[str] = aliases
        else:
            self.aliases: List[str] = ["Block"]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Raises your shield and blocks attacks until your next turn.",
            "If you are hit, you will lose stamina instead of HP.",
            "Params: None",
        ])

    def do_combat_action(self, game: Game, source_player: Character, params: List[Any]) -> None:
        from Game import TriggerFunc
        game.discord_connection.send_game_chat_sync(f"{source_player.combat_name} raises their shield.")
        source_player.assign_damage = BlockCommand.assign_damage
        game.once("before_player_combat", TriggerFunc(BlockCommand.detach_damage_replacement))

    @staticmethod
    def detach_damage_replacement(source_player=None, **kwargs):
        source_player.assign_damage = default_damage_assignment

    @staticmethod
    def assign_damage(game, source, target, damage):
        stamina_damage = min(damage, target.stamina)
        target.stamina = max(0, target.stamina - stamina_damage)
        remaining_damage = damage - stamina_damage
        target.health = max(0, target.health - remaining_damage)
        to_return = f"{target.combat_name}'s shield absorbs {stamina_damage} damage."
        if remaining_damage > 0:
            to_return = to_return + f"{target.name} takes {remaining_damage} damage."
        return to_return
