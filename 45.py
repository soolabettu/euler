import mytimeit
import math
import time


def solve() -> int:
    n = 286
    while True:
        formula = (n * (n + 1)) / 2
        p = (1 + math.sqrt(1 + 4 * 3 * 2 * formula)) // 6
        h = (1 + math.sqrt(1 + 4 * 2 * formula)) // 4

        f1 = p * (3 * p - 1) / 2
        f2 = h * (2 * h - 1)
        if formula == f1 and formula == f2:
            return formula

        n += 1


with mytimeit.MyTimer() as t:
    print(solve())
