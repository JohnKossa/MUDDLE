class Item:
    def __init__(self):
        self.quantity = 0
        self.max_stack_size = 0
        self.weight = 0
        self.name = "Item"
        self.template = None

    def describe(self):
        if self.template is None:
            return "This item has no template description"
        else:
            return "This needs to look up the description from the template"

    def use_effect(self, game, source_player, target_player):
        # describes what happens when a player does !use with the item
        pass

    def get_commands(self):
        # will add the use and drop commands
        return []


class Equipment(Item):
    def __init__(self):
        super().__init__()
        self.slot = None
        self.max_hitpoints = 100
        self.hit_points = 100
        self.active_effects = []
        self.resistances = {  # any resistance not specified is assumed to be 0

        }

    def use_effect(self, game, source_player, target_player):
        # equips the item
        pass

    def get_commands(self):
        # will add equip and unequip commands
        return super().get_commands() + []


class Weapon(Equipment):
    def __init__(self):
        super().__init__()
        self.slot = "Hand"

    def get_commands(self):
        # will add "attack" command
        return super().get_commands() + []


class Sword(Weapon):
    def __init__(self):
        super().__init__()
        self.default_attack = "slash"
        self.hit_bonus = {
            "slash": 0,
            "stab": 0
        }
        self.damage_bonus = {
            "slash": 0,
            "stab": 0
        }

    def get_commands(self):
        # will add slash, and stab commands
        return super().get_commands() + []


class Shield(Equipment):
    def __init__(self):
        super().__init__()
        self.slot = "Hand"

    def get_commands(self):
        # will add "block" command
        return super().get_commands() + []


class Armor(Equipment):
    def __init__(self):
        super().__init__()
        self.slot = "Body"
        self.conferred_resistances = { # resistances bestowed to user when equipped. assumed to be 0 if not specified

        }

    def get_commands(self):
        # will add "block" command
        return super().get_commands() + []