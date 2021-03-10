import random


def roll(count, faces, advantage=0):
    raw_rolls = []
    for i in range(count + abs(advantage)):
        raw_rolls.append(random.randint(1, faces))
    raw_rolls.sort()
    if advantage > 0:
        return sum(raw_rolls[advantage:])
    elif advantage < 0:
        return sum(raw_rolls[:advantage])
    else:
        return sum(raw_rolls)


def print_advantage_spread():
    for adv in range(-10, 11):
        print("advantage {}".format(adv))
        total = 0
        for i in range(100):
            total = total + roll(3, 6, advantage=adv)
        print("avg {}".format(total/100))

