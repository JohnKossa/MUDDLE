from __future__ import annotations
from typing import Any, Optional

from Game import Game
from game_objects.CombatEntity import CombatEntity
from game_objects.Commands.CombatCommands.CombatCommand import CombatOnlyCommand
from game_objects.StatusEffect import StatusEffect
from utils.Constanats import DamageTypes
from utils.TriggerFunc import TriggerFunc


class BlockCommand(CombatOnlyCommand):
    from game_objects.CombatEntity import CombatEntity

    def __init__(self, aliases: list[str] = None):
        super().__init__()
        self.combat_action_cost: int = 1
        if aliases is not None:
            self.aliases: list[str] = aliases
        else:
            self.aliases: list[str] = ["Block"]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Raises your shield and blocks attacks until your next turn.",
            "If you are hit, you will lose stamina instead of HP.",
            "Params: None",
        ])

    def command_valid(self, game: Game, source_player: CombatEntity, params: list[Any]) -> bool:
        # could optionally check for a shield or an item tha grants block, but might not be worth it
        return True

    def do_combat_action(self, game: Game, source_entity: CombatEntity, params: list[Any]) -> None:
        game.discord_connection.send_game_chat_sync(f"{source_entity.combat_name} raises their shield.")
        status = BlockingStatus(source_entity)
        source_entity.add_status(game, status)


class BlockingStatus(StatusEffect):
    def __init__(self, parent):
        super().__init__(parent)
        from utils.Constanats import Triggers
        self.hit_resistances = {
            DamageTypes.Pierce: 1,
            DamageTypes.Slash: 1
        }
        self.triggers = {
            Triggers.BeforeEntityCombat: TriggerFunc(self.tick),
            Triggers.LeaveRoom: TriggerFunc(self.remove_on_leave_room)
        }
        self.parent.assign_damage = BlockingStatus.assign_damage

    def tick(self, source_entity: Optional[CombatEntity] = None, game: Optional[Game] = None, **kwargs) -> None:
        if source_entity != self.parent:
            return
        from utils.CombatHelpers import assign_damage
        self.parent.assign_damage = assign_damage
        self.parent.status_effects.remove(self)
        self.parent = None
        self.detach_triggers(game)

    def remove_on_leave_room(self, source_entity: Optional[CombatEntity] = None, game: Optional[Game] = None, **kwargs) -> None:
        if source_entity != self.parent:
            return
        from utils.CombatHelpers import assign_damage
        self.parent.assign_damage = assign_damage
        self.parent.status_effects.remove(self)
        self.parent = None
        self.detach_triggers(game)

    @staticmethod
    def assign_damage(game, source, target, damage):
        from game_objects.Character.Character import Character
        stamina_damage = min(damage, target.stamina)
        target.stamina = max(0, target.stamina - stamina_damage)
        remaining_damage = damage - stamina_damage
        target.health = max(0, target.health - remaining_damage)
        if isinstance(target, Character):
            to_return = f"{target.combat_name}'s shield absorbs {stamina_damage} damage. ({target.display_stamina} pp left)"
        else:
            to_return = f"{target.combat_name}'s shield absorbs {stamina_damage} damage."
        if remaining_damage > 0:
            if isinstance(target, Character):
                to_return = to_return + f"{target.name} takes {remaining_damage} damage. ({target.display_health} hp left)"
            else:
                to_return = to_return + f"{target.name} takes {remaining_damage} damage."
        return to_return
