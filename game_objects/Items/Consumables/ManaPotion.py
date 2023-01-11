from game_objects.Items.Consumables.Consumable import Consumable


class ManaPotion(Consumable):
    def __init__(self):
        super().__init__()
        self.name = "ManaPotion"
        self.max_stack_size = 5
        self._basevalue = 50