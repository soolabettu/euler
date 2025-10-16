import mytimeit


import math


def solve(limit):
    """Find the grid dimensions under limit whose sub-rectangle count is closest to two million."""
    margin = 3000000
    area = 0
    nearest_dim = (0, 0)
    for i in range(1, limit):
        for j in range(1, i):
            part1 = math.factorial(i + 1) // (
                math.factorial(i + 1 - 2) * math.factorial(2)
            )
            part2 = math.factorial(j + 1) // (
                math.factorial(j + 1 - 2) * math.factorial(2)
            )
            rectangles = part1 * part2
            diff = abs(rectangles - 2000000)
            if diff < margin:
                margin = diff
                area = i * j
                nearest_dim = (i, j)

    return (area, nearest_dim)


import mytimeit

with mytimeit.MyTimer() as t:
    print(solve(100))
