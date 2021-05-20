from __future__ import annotations
from typing import Any, List, Optional

from Game import Game
from game_objects.Character.Character import Character
from game_objects.Commands.CombatCommands.CombatCommand import CombatOnlyCommand
from game_objects.StatusEffect import StatusEffect
from utils.Constanats import DamageTypes
from utils.TriggerFunc import TriggerFunc


class DodgeCommand(CombatOnlyCommand):
    from game_objects.CombatEntity import CombatEntity

    def __init__(self, aliases: List[str] = None):
        super().__init__()
        self.combat_action_cost: int = 1
        if aliases is not None:
            self.aliases: List[str] = aliases
        else:
            self.aliases: List[str] = ["Dodge"]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Attempts to dodge attacks until the beginning of your next turn.",
            "Costs 5 stamina to use.",
            "Params: None"
        ])

    def command_valid(self, game: Game, source_player: CombatEntity, params: List[Any]) -> bool:
        """Check if the command is still valid."""
        if source_player.stamina >= 5:
            return True
        return False

    def do_combat_action(self, game: Game, source_player: Character, params: List[Any]) -> None:
        if source_player.stamina < 5:
            game.discord_connection.send_game_chat_sync(f"{source_player.combat_name}'s stamina is too low.")
        else:
            source_player.stamina = source_player.stamina - 5
            game.discord_connection.send_game_chat_sync(f"{source_player.combat_name} dodges.")
            status = DodgeStatus(source_player)
            source_player.add_status(game, status)


class DodgeStatus(StatusEffect):
    def __init__(self, parent):
        super().__init__(parent)
        from utils.Constanats import Triggers
        self.hit_resistances = {
            DamageTypes.Bludgeon: 1,
            DamageTypes.Pierce: 1,
            DamageTypes.Slash: 1,
            DamageTypes.Electricity: 1,
            DamageTypes.Ice: 1,
            DamageTypes.Fire: 1
        }
        self.triggers = {
            Triggers.BeforeEntityCombat: TriggerFunc(self.detach_on_turn_start, self.parent),
            Triggers.LeaveRoom: TriggerFunc(self.detach_on_turn_start, self.parent)
        }

    def detach_on_turn_start(self, source_player: Optional[Character] = None, game: Optional[Game] = None, **kwargs) -> None:
        if source_player == self.parent:
            source_player.status_effects.remove(self)
            self.parent = None
            self.detach_triggers(game)