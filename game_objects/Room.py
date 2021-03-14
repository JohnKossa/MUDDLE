from game_objects.Combat import Combat
from game_objects.Items.Item import Item
from game_objects.Commands.PartialCombatCommands.TakeCommand import Take


class Room:
    def __init__(self, name=""):
        self.name = name
        self.template = None
        self.fixtures = []
        self.items = [Item()]
        self.combat = None

    def get_commands(self):
        to_return = []
        if len(self.items) > 0:
            to_return.append(Take())
        for fixture in self.fixtures:
            to_return.extend(fixture.get_commands())
        return to_return

    def start_combat(self, game):
        if self.combat is not None:
            return
        self.combat = Combat(players=self.get_players(game), enemies=self.get_enemies(game), room=self)
        self.combat.start(game)

    def end_combat(self):
        del self.combat
        self.combat = None

    def get_enemies(self, game):
        return [x for x in game.enemies if x.current_room == self]

    def get_players(self, game):
        return [x for x in game.players if x.current_room == self]
