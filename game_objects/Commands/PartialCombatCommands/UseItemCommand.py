from game_objects.Commands.PartialCombatCommands.PartialCombatCommand import PartialCombatCommand


class UseItem(PartialCombatCommand):
    # check if in combat
    # if in combat:
    #   check equipped items for one patching params[0]
    #   if exists:
    #       call the use function on the item
    #   else:
    #       return "Item not found in currently equipped items."
    # else:
    #   check bagged items and then equipped items for one matching params[0]
    #   if exits:
    #       call the use function on the item
    #   else:
    #       return "Item not found in bag or equipped items
    def __init__(self):
        super().__init__()
        self.aliases = [
            "UseItem",
            "Use",
        ]

    @classmethod
    def show_help(cls):
        return "\n".join([
            "Performs the default action of an item.",
            "If in combat, only works for equipped items",
            "If out of combat, works for any stored items as well",
            "Params:",
            "    0: The name of the item to use"
        ])

    def do_noncombat(self, game, params, message):
        return ""

    def do_combat_action(self, game, source_player, params):
        pass