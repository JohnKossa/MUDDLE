import datetime

from game_objects.Commands.CombatCommands.CombatCommand import PassCommand
from utils.AsyncHelpers import async_to_sync
from utils.Scheduler import ScheduledTask


class Combat:
    def __init__(self, players=[], enemies=[]):
        self.players = players
        self.enemies = enemies
        self.orders = {}
        self.round_schedule_object = None

    def process_round(self, game):
        # loop through all players and fill missing commands with passes
        pass_cmd = PassCommand()
        orders_filled = False
        for player in self.players:
            action_count = self.sum_actions_for_player(player)
            if action_count < player.actions:
                orders_filled = True
                actions_to_fill = player.actions - action_count
                for count in range(actions_to_fill):
                    self.orders[player].append((pass_cmd.do_action, [], pass_cmd.combat_action_cost))

        if orders_filled:
            # round filled via timer instead of full orders, notify that timer expired
            async_to_sync(game.discord_connection.send_game_chat, "Courtesy timer expired. Processing combat.", loop=game.aioloop)

        # TODO fill orders for all enemies

        initiative_list = [(x, x.initiative) for x in self.players + self.enemies]
        sorted_initiative_list = map(lambda y: y[0], sorted(initiative_list, key=lambda x: x[1]))
        for actor in sorted_initiative_list:
            for order in self.orders[actor]:
                # if order is still valid
                action = order[0]
                params = order[1]
                action(game, actor, params)
                # else
                #   perform pass
                # perform cleanup such as modifying items or removing dead enemies, etc
                pass

        if len(self.players) == 0:
            # all players dead or left room, end combat
            return
        if len(self.enemies) == 0:
            # all enemies dead, end combat
            return
        # clear initiative list, reset timer

    def add_player(self, game, player):
        # new player enters room
        # add to end of initiative order
        # notify player of remaining time on process_round
        pass

    def sum_actions_for_player(self, player):
        order_list = self.orders.get(player, [])
        if len(order_list) == 0:
            return 0
        return sum(x[2] for x in order_list)

    def accept_player_order(self, game, source_player, action, params, cost):
        # TODO check if player order is valid?
        current_action_costs = self.sum_actions_for_player(source_player)
        if current_action_costs + cost <= source_player.actions:
            self.orders[source_player] = self.orders.get(source_player, []).append((action, params, cost))

        all_actions_filled = True
        for player in self.players:
            if self.sum_actions_for_player(player) < player.actions:
                all_actions_filled = False

        if all_actions_filled:
            game.discord_connection.send_game_chat("All orders accepted.")
            game.scheduler.unschedule_task(self.round_schedule_object)
            self.round_schedule_object = None
            self.process_round(game)
        elif self.round_schedule_object is None:
            self.round_schedule_object = ScheduledTask(datetime.datetime.now()+datetime.timedelta(minutes=30), self.process_round, game)


class AttackAction:
    def __init__(self, name="attack", hit_bonus=0, dmg_type="bludgeon", dmg_roll=(1, 6), dmg_bonus=0, action_cost=1):
        self.name = name
        self.hit_bonus = hit_bonus
        self.dmg_type = dmg_type
        self.dmg_roll = dmg_roll
        self.dmg_bonus = dmg_bonus
        self.action_cost = action_cost
