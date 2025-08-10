import mytimeit
from functools import reduce
import operator


def solve() -> int:
    z = set()
    result = 0
    for i in range(1, 100):
        for j in range(1, 10000):
            k = i * j
            if k in z:
                continue

            s = str(i) + str(j) + str(k)
            if len(s) != 9:
                continue
            sorted_s = "".join(sorted(s, key=int))
            if sorted_s == "123456789":
                z.add(k)

    return sum(z)


with mytimeit.MyTimer() as t:
    print(solve())
