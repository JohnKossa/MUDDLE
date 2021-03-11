from utils.Dice import roll
from utils.AsyncHelpers import async_to_sync


class Combat:
    def __init__(self, players=[], enemies=[]):
        self.players = players
        self.enemies = enemies
        self.orders = {}

    def process_round(self, game):
        orders_filled = False
        for player in self.players:
            # loop through self.orders[player]
            # count the action_cost of all commands
            # for each action less than player.actions
            # add a "pass" command to the actions
            pass

        if orders_filled:
            # round filled via timer instead of full orders, notify that timer expired
            async_to_sync(game.discord_connection.send_game_chat, "Courtesy timer expired. Processing combat.", loop=game.aioloop)

        initiative_list = [(x, x.initiative) for x in self.players + self.enemies]
        sorted_initiative_list = map(lambda y: y[0], sorted(initiative_list, key=lambda x: x[1]))
        for actor in sorted_initiative_list:
            # get orders for actor
            # if order not valid
            #   perform pass order
            # else
            #   perform order
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

        # if all player orders filled
        #   say "All Orders Accepted"
        #   cancel scheduled process_round
        #   run process_round
        pass


class AttackAction:
    def __init__(self, name="attack", hit_bonus=0, dmg_type="bludgeon", dmg_roll=(1,6), dmg_bonus=0, action_cost=1):
        self.name = name
        self.hit_bonus = hit_bonus
        self.dmg_type = dmg_type
        self.dmg_roll = dmg_roll
        self.dmg_bonus = dmg_bonus
        self.action_cost = action_cost
