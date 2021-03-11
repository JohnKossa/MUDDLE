from game_objects.Combat import Combat


class Room:
    def __init__(self, name=""):
        self.name = name
        self.template = None
        self.fixtures = []
        self.items = []
        self.combat = None

    def get_commands(self):
        to_return = []
        for fixture in self.fixtures:
            to_return = to_return + fixture.get_commands()
        return to_return

    def start_combat(self, game):
        self.combat = Combat(players=self.get_players(game), enemies=self.get_enemies(game))
        self.combat.start(game)

    def get_enemies(self, game):
        return [x for x in game.enemies if x.room == self]

    def get_players(self, game):
        return [x for x in game.players if x.current_room == self]
