class Item:
    def __init__(self):
        self.quantity = 1
        self.max_stack_size = 1
        self.weight = 0
        self.name = "Item"
        self.template = None

    def describe(self):
        # TODO lookup item from template
        if self.template is None:
            return f"a {self.name}"
        else:
            return "This needs to look up the description from the template"

    def able_to_join(self, other):
        if self.name != other.name:
            return False
        if self.quantity + other.quantity > self.max_stack_size:
            return False
        # TODO when we add durability, if durability doesn't match, return false
        # TODO when we add custom effects (magic), return false if either has one
        return True

    def take_count_from_stack(self, count):
        if count > self.quantity:
            return None
        if count == self.quantity:
            return self
        self.quantity = self.quantity - count
        new_item = Item()
        new_item.quantity = count
        new_item.max_stack_size = self.max_stack_size
        new_item.weight = self.weight
        new_item.name = self.name
        new_item.template = self.template
        return new_item

    def use_effect(self, game, source_player, target_player):
        # describes what happens when a player does !use with the item
        pass

    def get_commands(self):
        # will add the use and drop commands
        return []
