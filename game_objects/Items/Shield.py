from game_objects.Items.Equipment import Equipment


class Shield(Equipment):
    def __init__(self):
        super().__init__()
        self.slot = "Hand"

    def get_commands(self):
        # will add "block" command
        return super().get_commands() + []