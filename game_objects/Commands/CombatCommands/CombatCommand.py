from game_objects.Commands.Command import Command


class CombatOnlyCommand(Command):
    def __init__(self):
        super().__init__()
        self.combat_action_cost = 1

    def do_action(self, game, params, message):
        from discord_objects.DiscordUser import UserUtils
        user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        if user is None:
            return "You are not listed as a user in this game."
        character = user.current_character
        room = character.current_room
        combat = room.combat
        combat.accept_player_order(game, character, self.do_combat_action, [], self.combat_action_cost)
        return "Order Accepted"

    def do_combat_action(self, game, source_player, params):
        raise Exception("Not yet implemented")
