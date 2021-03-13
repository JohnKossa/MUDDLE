class Item:
    def __init__(self):
        self.quantity = 1
        self.max_stack_size = 1
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


