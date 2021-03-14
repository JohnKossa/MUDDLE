from game_objects.Commands.PartialCombatCommands.PartialCombatCommand import PartialCombatCommand


class Take(PartialCombatCommand):
    def __init__(self):
        super().__init__()
        self.aliases = [
            "Take",
            "Pickup"
        ]
        self.combat_action_cost = 1

    def show_help(cls):
        return "\n".join([
            "Picks up an item in the current room and adds it to your bag.",
            "Params:",
            "    0: Item Name",
        ])

    def do_noncombat(self, game, params, message):
        from discord_objects.DiscordUser import UserUtils
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        player = discord_user.current_character
        target_item = params[0]
        room = player.current_room
        items = room.items
        matched_item = next(filter(lambda  x: x.name.lower() == target_item.lower(), items), None)
        if matched_item is None:
            return "Item not found"
        player.inventory.bag[matched_item] = matched_item.quantity
        room.items.remove(matched_item)
        return f"Picked up {matched_item.quantity} {matched_item.name}"

    def do_combat_action(self, game, source_player, params):
        target_item = params[0]
        room = source_player.current_room
        items = room.items
        matched_item = next(filter(lambda  x: x.name.lower() == target_item.lower(), items), None)
        if matched_item is None:
            game.discord_connection.send_game_chat_sync(f"{source_player.name} attempted to pick up a picked up  a {target_item} but could not find any.")
            return
        source_player.inventory.bag[matched_item] = matched_item.quantity
        room.items.remove(matched_item)
        game.discord_connection.send_game_chat_sync(f"{source_player.name} picked up {matched_item.quantity} {matched_item.name}")
