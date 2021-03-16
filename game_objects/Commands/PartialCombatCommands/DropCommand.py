from game_objects.Commands.PartialCombatCommands.PartialCombatCommand import PartialCombatCommand
from utils.ListHelpers import get_by_index


class Drop(PartialCombatCommand):
    def __init__(self):
        super().__init__()
        self.aliases = [
            "Drop",
            "Discard"
        ]
        self.combat_action_cost = 0

    @classmethod
    def show_help(cls):
        return "\n".join([
            "Not yet implemented: Will drop a held or stored item on the floor of the current room ",
            "Params:",
            "    0: Item Name",
            "    1: (optional) Quantity"
        ])

    def do_noncombat(self, game, params, message):
        from discord_objects.DiscordUser import UserUtils
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        player = discord_user.current_character
        target_item = params[0]
        room = player.current_room
        player_bag = player.inventory.bag
        matched_item = player.inventory.get_item_by_name(target_item)
        if matched_item is None:
            return "Item not found"
        bag_quantity = player_bag[matched_item]
        try:
            quantity = int(get_by_index(params, 1))
            if quantity > bag_quantity:
                quantity = bag_quantity
        except TypeError:
            quantity = bag_quantity

        bag_quantity = bag_quantity - quantity
        if bag_quantity == 0:
            player_bag.pop(matched_item)

        room.items.append(matched_item)
        return f"Dropped {quantity} {matched_item.name}"

    def do_combat_action(self, game, source_player, params):
        target_item = params[0]
        room = source_player.current_room
        player_bag = source_player.inventory.bag
        matched_item = source_player.inventory.get_item_by_name(target_item)
        if matched_item is None:
            game.discord_connection.send_game_chat_sync(f"{source_player.name} attempted to drop an item, but could find a {target_item} in their inventory")
        bag_quantity = player_bag[matched_item]
        try:
            quantity = int(params[1])
            if quantity > bag_quantity:
                quantity = bag_quantity
        except IndexError:
            quantity = bag_quantity
        except TypeError:
            quantity = bag_quantity

        bag_quantity = bag_quantity - quantity
        if bag_quantity == 0:
            player_bag.pop(matched_item)

        room.items.append(matched_item)
        game.discord_connection.send_game_chat_sync(f"{source_player.name} dropped {quantity} {matched_item.name}")