from __future__ import annotations
import random


def roll(count: int, faces: int, advantage: int = 0) -> int:
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


def get_random(luck: int = 0) -> float:
    if luck == 0:
        return random.random()
    raw_rolls = []
    for i in range(1 + abs(luck)):
        raw_rolls.append(random.random())
    raw_rolls.sort()
    if luck > 0:
        return raw_rolls[-1]
    else:
        return raw_rolls[0]


def print_advantage_spread() -> None:
    for adv in range(-10, 11):
        print(f"advantage {adv}")
        total = 0
        for i in range(1000):
            total = total + roll(1, 20, advantage=adv)
        print(f"avg {total/1000}")


def print_diff_spread() -> None:
    trials = 100000
    diffs = {}
    for i in range(-19, 20):
        diffs[str(i)] = 0
    for i in range(trials):
        diff = roll(1, 20) - roll(1, 20)
        diffs[str(diff)] = diffs[str(diff)] + 1
    for i in range(-19, 20):
        diffs[str(i)] = (diffs[str(i)] / trials)*100
    print(str(diffs))


if __name__ == "__main__":
    # print_advantage_spread()
    print_diff_spread()
