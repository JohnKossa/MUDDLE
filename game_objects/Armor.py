from .Item import Item


class Armor(Item):
    def __init__(self):
        self.resistances = {
            "bludgeoning": 0,
            "slashing": 0,
            "piercing": 0,
            "fire": 0,
            "lightning": 0
        }
