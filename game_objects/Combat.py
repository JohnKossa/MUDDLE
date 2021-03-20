import datetime
import random

from game_objects.Commands.CombatCommands.AttackCommand import AttackCommand
from game_objects.Commands.CombatCommands.PassCommand import PassCommand
from utils.Scheduler import ScheduledTask, time_until_event


class Combat:
    def __init__(self, players=[], enemies=[], room=None):
        self.players = players
        self.enemies = enemies
        self.orders = {}
        self.initiatives = {}
        self.round_schedule_object = None
        self.room = room

    def start(self, game):
        if len(self.players) == 0:
            game.discord_connection.send_game_chat_sync("Could not start combat. There are no players in the room.")
            return
        if len(self.enemies) == 0:
            game.discord_connection.send_game_chat_sync("Could not start combat. There are no enemies in the room.")
            return

        for player in self.players:
            self.orders[player] = []
        for enemy in self.enemies:
            self.orders[enemy] = []
        game.discord_connection.send_game_chat_sync(f"Started combat in room {self.room.name}.")
        self.round_schedule_object = ScheduledTask(datetime.datetime.now() + datetime.timedelta(minutes=10),
                                                   self.process_round, game)
        game.scheduler.schedule_task(self.round_schedule_object)

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
                    self.orders[player].append((pass_cmd.do_combat_action, [], pass_cmd.combat_action_cost))

        if orders_filled:
            # round filled via timer instead of full orders, notify that timer expired
            game.discord_connection.send_game_chat_sync("Courtesy timer expired. Processing combat.")

        for enemy in self.enemies:
            action_count = self.sum_actions_for_player(enemy)
            failsafe = 100
            while action_count < enemy.actions and failsafe > 0:
                chosen_action = enemy.get_action()
                if action_count + chosen_action.action_cost <= enemy.actions:
                    cmd = AttackCommand(chosen_action)
                    target_player = random.choice(self.players).name  # TODO randomly targeting players, switch for intelligent decision later
                    self.orders[enemy].append((cmd.do_combat_action, [target_player], cmd.combat_action_cost))
                failsafe = failsafe - 1
                action_count = self.sum_actions_for_player(enemy)

        for entity in self.players + self.enemies:
            if entity not in self.initiatives:
                self.initiatives[entity] = entity.initiative

        initiative_list = [(x, self.initiatives[x]) for x in self.players + self.enemies]
        sorted_initiative_list = map(lambda y: y[0], sorted(initiative_list, key=lambda x: x[1]))
        for actor in sorted_initiative_list:
            for order in self.orders[actor]:
                # if order is still valid
                action = order[0]
                params = order[1]
                action(game, actor, params)
                # else
                #   perform pass

                # cleanup
                # check for dead enemies
                for enemy in self.enemies:
                    if enemy.health <= 0:
                        enemy.dead = True
                        self.enemies.remove(enemy)
                        game.discord_connection.send_game_chat_sync(f"{enemy.name} was slain")
                        # drop treasure from loot table

                for player in self.players:
                    if player.health <= 0:
                        player.dead = True
                        self.players.remove(player)
                        game.discord_connection.send_game_chat_sync(f"{player.name} has fallen in combat")
                        # drop treasure form player inventory

                # TODO additional cleanup for items

        # post-round actions
        game.trigger("round_end", room=self.room)

        self.players = list(filter(lambda x: not x.dead, self.room.get_players(game)))
        self.enemies = list(filter(lambda x: not x.dead, self.room.get_enemies(game)))

        initiative_keys = list(self.initiatives.keys())
        for k in initiative_keys:
            if k not in self.players + self.enemies:
                self.initiatives.pop(k)

        # all players dead or left room, end combat
        if len(self.players) == 0:
            game.discord_connection.send_game_chat_sync("All players retreated or dead. Ending combat.")
            self.room.end_combat()
            return
        # all enemies dead, end combat
        if len(self.enemies) == 0:
            game.discord_connection.send_game_chat_sync("All enemies defeated. Ending combat.")
            self.room.end_combat()
            return

        # clear orders, reset timer
        game.discord_connection.send_game_chat_sync("Round complete.")
        self.orders = {}
        for player in self.players:
            self.orders[player] = []
        for enemy in self.enemies:
            self.orders[enemy] = []
        self.round_schedule_object = ScheduledTask(datetime.datetime.now() + datetime.timedelta(minutes=10),
                                                   self.process_round, game)
        game.scheduler.schedule_task(self.round_schedule_object)
        remaining_time = time_until_event(self.round_schedule_object)
        game.discord_connection.send_game_chat_sync(f"Accepting orders for next round in {remaining_time[0]} minutes and {remaining_time[1]} seconds")

    def add_player(self, game, player):
        self.players.append(player)
        self.orders[player] = []
        remaining_time = time_until_event(self.round_schedule_object)
        game.discord_connection.send_game_chat_sync(f"Combat will process in {remaining_time[0]} minutes, and {remaining_time[1]} seconds")

    def sum_actions_for_player(self, player):
        if player not in self.orders.keys() and player in self.players:
            self.orders[player] = []
        order_list = self.orders[player]
        if order_list is None:
            return 0
        if len(order_list) == 0:
            return 0
        return sum(x[2] for x in order_list)

    def accept_player_order(self, game, source_player, action, params, cost):
        # TODO check if player order is valid?
        # TODO probably bounce that check back to a function on the action itself
        possible_targets = [x.name for x in self.players + self.enemies]

        current_action_costs = self.sum_actions_for_player(source_player)
        if current_action_costs + cost <= source_player.actions:
            if self.orders[source_player] is None:
                self.orders[source_player] = []
            self.orders[source_player].append((action, params, cost))
        else:
            game.discord_connection.send_game_chat_sync("Order would overrun allowed action count", tagged_users=[source_player.discord_user])
            return

        all_actions_filled = True
        for player in self.players:
            if self.sum_actions_for_player(player) < player.actions:
                all_actions_filled = False

        if all_actions_filled:
            game.discord_connection.send_game_chat_sync("All orders accepted.")
            game.scheduler.unschedule_task(self.round_schedule_object)
            self.round_schedule_object = None
            self.process_round(game)
        elif self.round_schedule_object is None:
            self.round_schedule_object = ScheduledTask(datetime.datetime.now()+datetime.timedelta(minutes=10), self.process_round, game)
            game.scheduler.schedule_task(self.round_schedule_object)


class AttackAction:
    def __init__(self, name="attack", hit_bonus=0, dmg_type="bludgeon", dmg_roll=(1, 6), dmg_bonus=0, action_cost=1):
        self.name = name
        self.hit_bonus = hit_bonus
        self.dmg_type = dmg_type
        self.dmg_roll = dmg_roll
        self.dmg_bonus = dmg_bonus
        self.action_cost = action_cost
