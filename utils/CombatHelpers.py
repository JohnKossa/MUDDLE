from utils.Dice import roll


def calculate_damage(attack, hit_resistances, dmg_resistances):
    matched_hit_resistance = hit_resistances.get(attack.dmg_type, 0)
    matched_dmg_resistance = dmg_resistances.get(attack.dmg_type, 0)
    hit_roll = roll(1, 20, advantage=attack.hit_bonus)
    miss_roll = roll(1, 20, advantage=matched_hit_resistance)
    if hit_roll <= miss_roll:
        print("Missed")
        return 0
    print("Hit!")
    damage_roll = roll(attack.dmg_roll[0], attack.dmg_roll[1], advantage=(attack.dmg_bonus - matched_dmg_resistance))
    return damage_roll


def sum_resistances(set1, set2):
    to_return = {}
    known_keys = list(set(set1.keys()) | set(set2.keys()))
    for k in known_keys:
        to_return[k] = set1.get(k, 0) + set2.get(k, 0)
    return to_return
