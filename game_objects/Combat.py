from __future__ import annotations
import datetime
import random
from typing import Any, Callable, Dict, List,  Optional

import Game
from game_objects.Character import Character
from game_objects.Enemy import Enemy
from game_objects.CombatEntity import CombatEntity
from game_objects.Commands.CombatCommands.AttackCommand import AttackCommand
from game_objects.Commands.CombatCommands.PassCommand import PassCommand
from utils.Scheduler import ScheduledTask, time_until_event


class Combat:
    def __init__(self, players=[], enemies=[], room=None):
        from game_objects.Room import Room
        self.players: List[Character] = players
        self.enemies: List[Enemy] = enemies
        self.orders: dict = {}
        self.initiatives: dict = {}
        self.round_schedule_object: Optional[ScheduledTask] = None
        self.room: Room = room

    def start(self, game: Game) -> None:
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
        self.disambiguate_enemies()
        game.discord_connection.send_game_chat_sync(f"Started combat in room {self.room.name}.")
        self.round_schedule_object = ScheduledTask(datetime.datetime.now() + datetime.timedelta(minutes=10),
                                                   self.process_round, game)
        game.scheduler.schedule_task(self.round_schedule_object)

    def disambiguate_enemies(self) -> None:
        all_enemies_in_room: List[Enemy] = self.enemies.copy()
        all_names: Dict[str, List[Enemy]] = {}
        while len(all_enemies_in_room) > 0:
            current_enemy = all_enemies_in_room[0]
            all_names[current_enemy.name] = list(filter(lambda x: x.name == current_enemy.name, all_enemies_in_room))
            for enemy in all_names[current_enemy.name]:
                all_enemies_in_room.remove(enemy)
        for name, lst in all_names.items():
            if len(lst) == 1:
                lst[0].disambiguation_num = 0
                continue
            for i in range(len(lst)):
                lst[i].disambiguation_num = i + 1

    def fill_unused_player_orders(self, player: Character) -> bool:
        pass_cmd = PassCommand()
        action_count = self.sum_actions_for_entity(player)
        if action_count < player.actions:
            actions_to_fill = player.actions - action_count
            for count in range(actions_to_fill):
                self.orders[player].append((pass_cmd.do_combat_action, [], pass_cmd.combat_action_cost))
            return True
        return False

    def determine_enemy_actions(self):
        for enemy in self.enemies:
            action_count = self.sum_actions_for_entity(enemy)
            failsafe = 100
            while action_count < enemy.actions and failsafe > 0:
                chosen_action = enemy.get_action()
                if action_count + chosen_action.action_cost <= enemy.actions:
                    cmd = AttackCommand(chosen_action)
                    target_player = random.choice(self.players).combat_name  # TODO randomly targeting players, switch for intelligent decision later
                    self.orders[enemy].append((cmd.do_combat_action, [target_player], cmd.combat_action_cost))
                failsafe = failsafe - 1
                action_count = self.sum_actions_for_entity(enemy)

    def cleanup_dead_enemies(self, game: Game):
        for enemy in self.enemies:
            if enemy.health <= 0:
                enemy.dead = True
                game.discord_connection.send_game_chat_sync(f"{enemy.combat_name} was slain")
                if enemy.loot_table:
                    dropped_items = enemy.loot_table.roll_drops()
                    if len(dropped_items):
                        game.discord_connection.send_game_chat_sync("Some items clatter to the floor.")
                        self.room.items = self.room.items + dropped_items
                self.enemies.remove(enemy)
                game.trigger("enemy_defeated", source_enemy=enemy)

    def cleanup_dead_players(self, game: Game):
        for player in self.players:
            if player.health <= 0:
                player.dead = True
                game.discord_connection.send_game_chat_sync(f"{player.combat_name} has fallen in combat")
                dropped_items = player.inventory.generate_loot_table().roll_drops()
                if len(dropped_items):
                    game.discord_connection.send_game_chat_sync("Some items clatter to the floor.")
                    self.room.items = self.room.items + dropped_items
                self.players.remove(player)
                game.trigger("player_defeated", source_player=player)

    def process_round(self, game: Game) -> None:
        # loop through all players and fill missing commands with passes
        filled_orders_for_player = False
        for player in self.players:
            filled_orders_for_player = filled_orders_for_player or self.fill_unused_player_orders(player)

        if filled_orders_for_player:
            # round filled via timer instead of full orders, notify that timer expired
            game.discord_connection.send_game_chat_sync("Courtesy timer expired. Processing combat.")

        self.determine_enemy_actions()

        combat_entities: List[CombatEntity] = self.players + self.enemies

        for entity in combat_entities:
            if entity not in self.initiatives:
                self.initiatives[entity] = entity.initiative

        initiative_list = [(x, self.initiatives[x]) for x in combat_entities]
        sorted_initiative_list = map(lambda y: y[0], sorted(initiative_list, key=lambda x: x[1]))
        for actor in sorted_initiative_list:
            if actor.dead:
                continue
            if type(actor) is Character:
                game.trigger("before_player_combat", source_player=actor, room=self.room)
            for order in self.orders[actor]:
                # if order is still valid
                action = order[0]
                params = order[1]
                action(game, actor, params)
                # else
                #   perform pass

                # cleanup
                self.cleanup_dead_enemies(game)
                self.cleanup_dead_players(game)

                # TODO additional cleanup for items
            if type(actor) is Character:
                game.trigger("after_player_combat", source_player=actor)

        # post-round actions
        game.trigger("round_end", room=self.room)

        self.players = list(filter(lambda x: not x.dead, self.room.get_characters(game)))
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

    def add_player(self, game: Game, player: Character) -> None:
        self.players.append(player)
        self.orders[player] = []
        remaining_time = time_until_event(self.round_schedule_object)
        game.discord_connection.send_game_chat_sync(f"Combat will process in {remaining_time[0]} minutes, and {remaining_time[1]} seconds")

    def sum_actions_for_entity(self, actor: CombatEntity) -> int:
        if actor not in self.orders.keys() and actor in self.players:
            self.orders[actor] = []
        order_list = self.orders[actor]
        if order_list is None:
            return 0
        if len(order_list) == 0:
            return 0
        return sum(x[2] for x in order_list)

    def accept_player_order(self, game: Game, source_player: Character, action: Callable, params: List[Any], cost: int):
        # TODO check if player order is valid?
        # TODO probably bounce that check back to a function on the action itself
        possible_targets: List[str] = [x.combat_name for x in self.players + self.enemies]

        current_action_costs = self.sum_actions_for_entity(source_player)
        if current_action_costs + cost <= source_player.actions:
            if self.orders[source_player] is None:
                self.orders[source_player] = []
            self.orders[source_player].append((action, params, cost))
        else:
            game.discord_connection.send_game_chat_sync("Order would overrun allowed action count", tagged_users=[source_player.discord_user])
            return

        all_actions_filled = True
        for player in self.players:
            if self.sum_actions_for_entity(player) < player.actions:
                all_actions_filled = False

        if all_actions_filled:
            game.discord_connection.send_game_chat_sync("All orders accepted.")
            game.scheduler.unschedule_task(self.round_schedule_object)
            self.round_schedule_object = None
            self.process_round(game)
        elif self.round_schedule_object is None:
            self.round_schedule_object = ScheduledTask(datetime.datetime.now()+datetime.timedelta(minutes=10), self.process_round, game)
            game.scheduler.schedule_task(self.round_schedule_object)
