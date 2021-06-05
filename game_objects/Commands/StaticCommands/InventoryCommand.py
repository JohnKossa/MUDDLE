import discord

import Game
from game_objects.Commands.Command import Command


class InventoryCommand(Command):
    def __init__(self):
        super().__init__()
        self.aliases = ["Inventory", "Items", "Bag"]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Lists your equipped items and the contents of your bags.",
            "Params: None"
        ])

    def do_action(self, game: Game, params: list[str], message: discord.Message) -> str:
        from discord_objects.DiscordUser import UserUtils
        from utils.Constanats import EquipmentSlots
        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        player = discord_user.current_character
        player.inventory.consolidate_items()
        to_return = ""
        if len(player.inventory.equipment.values()) > 0:
            to_return = to_return + "Equipment:\n"
        for k, v in player.inventory.equipment.items():
            if v is not None and k != EquipmentSlots.Belt:
                to_return = to_return + k.capitalize()+": "+v.name+"\n"
            if k == EquipmentSlots.Belt and len(v) > 0:
                to_return = to_return + "Belt:"
                for item_stack in player.inventory.equipment[EquipmentSlots.Belt]:
                    to_return = to_return + f"\n{item_stack.quantity}x {item_stack.name}"
        if len(player.inventory.bag) > 0:
            to_return = to_return + "\nBag:"
        for item_stack in player.inventory.bag:
            to_return = to_return + f"\n{item_stack.quantity}x {item_stack.name}"
        return to_return
