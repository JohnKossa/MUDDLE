class Room:
    def __init__(self, name=""):
        self.name = name
        self.template = None
        self.fixtures = []
        self.combat = None

    def get_commands(self):
        to_return = []
        for fixture in self.fixtures:
            to_return = to_return + fixture.get_commands()
        return to_return
