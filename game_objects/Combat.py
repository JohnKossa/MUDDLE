from utils.Dice import roll

class Combat:
    def __init__(self, players=[], enemies=[]):
        self.players = players
        self.enemies = enemies

    def calculate_damage(self, attack, hit_resistances, dmg_resistances):
        matched_hit_resistance = hit_resistances.get(attack.dmg_type, 0)
        matched_dmg_resistance = dmg_resistances.get(attack.dmg_type, 0)
        hit_roll = roll(1, 20, advantage=attack.hit_bonus)
        miss_roll = roll(1, 20, advantage=matched_hit_resistance)
        if hit_roll <= miss_roll:
            print("missed")
            return 0
        print("We Hit!")
        damage_roll = roll(attack.dmg_roll[0], attack.dmg_roll[1], advantage=(attack.dmg_bonus - matched_dmg_resistance))
        return damage_roll


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


class AttackAction:
    def __init__(self, name="attack", hit_bonus=0, dmg_type="bludgeon", dmg_roll=(1,6), dmg_bonus=0, action_cost=1):
        self.name = name
        self.hit_bonus = hit_bonus
        self.dmg_type = dmg_type
        self.dmg_roll = dmg_roll
        self.dmg_bonus = dmg_bonus
        self.action_cost = action_cost
