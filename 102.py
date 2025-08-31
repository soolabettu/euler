import mytimeit
from math import log10


def contains_origin(p1, p2, p3):
    def area(x1, y1, x2, y2, x3, y3):
        return abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0

    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    A = area(x1, y1, x2, y2, x3, y3)
    A1 = area(0, 0, x2, y2, x3, y3)
    A2 = area(x1, y1, 0, 0, x3, y3)
    A3 = area(x1, y1, x2, y2, 0, 0)

    return abs(A - (A1 + A2 + A3)) < 1e-9


def solve():
    ans = 0
    with open("0102_triangles.txt", "r") as f:
        for i, line in enumerate(f):
            (
                x1,
                y1,
                x2,
                y2,
                x3,
                y3,
            ) = map(int, line.split(","))
            ans += contains_origin((x1, y1), (x2, y2), (x3, y3))

    return ans


with mytimeit.MyTimer() as t:
    print(solve())
