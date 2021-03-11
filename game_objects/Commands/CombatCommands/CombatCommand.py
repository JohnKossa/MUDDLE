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
        combat.accept_player_order(game, character, self.do_combat_action, self.combat_action_cost)

    def do_combat_action(self, game, source_player, params):
        pass


class PassCommand(CombatOnlyCommand):
    def __init__(self):
        super().__init__()

    def do_combat_action(self, game, source_player, params):
        source_player.health += (source_player.max_health - source_player.health)*.1
        source_player.stamina += (source_player.max_stamina - source_player.stamina)*.1
        source_player.mana += (source_player.max_mana - source_player.mana)*.1


class AttackCommand(CombatOnlyCommand):
    def __init__(self, attack_action):
        super().__init__()
        self.combat_action_cost = attack_action.action_cost
        self.attack_action = attack_action

    def do_combat_action(self, game, source_player, params):
        # look up target from room by name
        # get resistance from target
        enemies = source_player.current_room.combat.enemies
        target = enemies[0]
        hit_resistance = sum_resistances(target.natural_armor.get("hit", {}), target.armor_bonus.get("hit", {}))
        dmg_resistance = sum_resistances(target.natural_armor.get("dmg", {}), target.armor_bonus.get("dmg", {}))
        damage = calculate_damage(self.attack_action, hit_resistance, dmg_resistance)
        target.health = max(0, target.health-damage)