from __future__ import annotations
from typing import Any, List, Optional

import Game
from game_objects.Character import Character
from game_objects.Combat import Combat
from game_objects.Commands.Command import Command
from game_objects.Commands.PartialCombatCommands.TakeCommand import Take
from game_objects.Enemy import Enemy


class Room:
    def __init__(self, name: str = ""):
        from game_objects.RoomFixture import Fixture
        from game_objects.Items.Item import Item
        self.name: str = name
        self.template: Any = None
        self.fixtures: List[Fixture] = []
        self.items: List[Item] = []
        self.combat: Optional[Combat] = None

    def get_commands(self) -> List[Command]:
        to_return = []
        if len(self.items) > 0:
            to_return.append(Take())
        for fixture in self.fixtures:
            to_return.extend(fixture.get_commands())
        return to_return

    def start_combat(self, game: Game) -> None:
        if self.combat is not None:
            return
        self.combat = Combat(players=self.get_players(game), enemies=self.get_enemies(game), room=self)
        self.combat.start(game)

    def end_combat(self) -> None:
        del self.combat
        self.combat = None

    def get_enemies(self, game) -> List[Enemy]:
        return [x for x in game.enemies if x.current_room == self]

    def get_players(self, game) -> List[Character]:
        return [x for x in game.players if x.current_room == self]
