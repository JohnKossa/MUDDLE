class Combat:
    def __init__(self, players=[], enemies=[]):
        self.players = players
        self.enemies = enemies

    def process_round(self, game):
        # for each player who doesn't have all their orders
        #   fill missing orders with "pass"
        #   say "Courtesy timer expired. Processing combat"
        # sort players and enemies by initiative
        # for player or enemy in initiative order
        #   if order not valid
        #       perform "pass" order
        #   if order still valid
        #       perform order
        #   perform cleanup such as modifying items or removing dead enemies, etc
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

    def accept_player_order(self, game):
        # if player orders valid
        #   add player order to orders queue
        # else
        #   respond with order error
        # if all player orders filled
        #   say "All Orders Accepted"
        #   cancel scheduled process_round
        #   run process_round
        pass
