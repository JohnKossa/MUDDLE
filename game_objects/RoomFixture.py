class Fixture:
    # things you find in rooms like torch sconces, tables
    # they belong to the room and grant additional contextual actions to players in the room
    def __init__(self):
        self.template = None

    def get_commands(self):
        return []
