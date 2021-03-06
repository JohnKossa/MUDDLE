from game_objects.Items.Equipment import Equipment


class Armor(Equipment):
    def __init__(self):
        super().__init__()
        self.slot = "Body"
        self.conferred_resistances = { # resistances bestowed to user when equipped. assumed to be 0 if not specified

        }

    def get_commands(self):
        return super().get_commands() + []