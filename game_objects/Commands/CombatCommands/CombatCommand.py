import random

from game_objects.Commands.Command import Command
from utils.CombatHelpers import calculate_damage, sum_resistances


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
        pass


class PassCommand(CombatOnlyCommand):
    def __init__(self):
        super().__init__()
        self.aliases = ["Pass"]

    def do_combat_action(self, game, source_player, params):
        source_player.health += (source_player.max_health - source_player.health)*.1
        source_player.stamina += (source_player.max_stamina - source_player.stamina)*.1
        source_player.mana += (source_player.max_mana - source_player.mana)*.1
        game.discord_connection.send_game_chat_sync(f"{source_player} passes. Stats partially restored.")


class AttackCommand(CombatOnlyCommand):
    def __init__(self, attack_action, aliases=None):
        super().__init__()
        self.combat_action_cost = attack_action.action_cost
        self.attack_action = attack_action
        if aliases is not None:
            self.aliases = aliases
        else:
            self.aliases = [
                "Attack",
                "Atk"
            ]

    @classmethod
    def show_help(cls):
        # TODO Correct this
        return "\n".join([
            "Performs the default attack for the weapon against the specified target.",
            "If no target is specified, the attack will target the first valid enemy",
            "Params:",
            "   0: Name of the enemy to attack (optional)"
        ])

    def do_combat_action(self, game, source_player, params):
        from game_objects.Enemy import Enemy
        enemies = source_player.current_room.combat.enemies
        players = source_player.current_room.combat.players
        target = None
        if len(params):
            for enemy in enemies:
                if enemy.name == params[0]:
                    target = enemy
            for player in players:
                if player.name == params[0]:
                    target = player
        elif type(source_player).__name__ == "Character":
            if len(enemies) == 0:
                return
            target = random.choice(enemies)
        elif type(source_player).__name__ == "Enemy" or issubclass(type(source_player), Enemy):
            if len(players) == 0:
                return
            target = random.choice(players)
        hit_resistance = target.resistances["hit"]
        dmg_resistance = target.resistances["dmg"]
        damage = calculate_damage(self.attack_action, hit_resistance, dmg_resistance)
        output = f"{source_player.name} uses {self.attack_action.name}. "
        output = output + ("It misses." if damage == 0 else f"{target.name} takes {damage} damage.")
        game.discord_connection.send_game_chat_sync(output)
        target.health = max(0, target.health-damage)
