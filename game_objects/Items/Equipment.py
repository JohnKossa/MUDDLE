from game_objects.Items.Item import Item


class Equipment(Item):
    def __init__(self):
        super().__init__()
        self.slot = None
        self.max_hitpoints = 100
        self.hit_points = 100
        self.active_effects = []
        self.resistances = {  # any resistance not specified is assumed to be 0

        }

    def use_effect(self, game, source_player, params):
        # equips the item
        pass

    def get_commands(self):
        # will add equip and unequip commands
        return super().get_commands() + []