from game_objects.Items.Equipment import Equipment


class Armor(Equipment):
    def __init__(self):
        super().__init__()
        self.slot = "Body"
        # resistances bestowed to user when equipped. assumed to be 0 if not specified
        self.damage_resistances = {}
        self.hit_resistances = {}

    def get_commands(self):
        return super().get_commands() + []
