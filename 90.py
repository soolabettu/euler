from mytimeit import MyTimer
from itertools import combinations
from math import comb

import itertools


def solve():
    """Return the number of distinct cube arrangements that can display all two-digit squares.

    This enumerates every 6-digit combination that can be engraved on a given cube face, and
    counts the unique unordered cube pairs that can render the square numbers 01, 04, 09, 16,
    25, 36, 49, and 81. Faces containing a 6 or 9 are considered interchangeable, matching the
    original problem's allowance for rotating the cube to reinterpret one as the other.
    """
    d1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    d2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    pairs = [(0, 1), (0, 4), (0, 9), (1, 6), (2, 5), (3, 6), (4, 9), (4, 6), (8, 1)]

    def all_pairs_possible(c1, c2):
        """Check whether two cube digit selections can display every required square.

        Parameters
        ----------
        c1, c2 : iterable[int]
            The six digits present on cube 1 and cube 2, respectively.

        Returns
        -------
        bool
            True if, after accounting for the 6/9 interchangeability, each square number in
            `pairs` can be displayed with one digit on each cube; False otherwise.
        """
        e1 = list(c1)
        e2 = list(c2)
        if 6 in e1 and 9 not in e1:
            e1.append(9)

        if 6 in e2 and 9 not in e2:
            e2.append(9)

        if 9 in e1 and 6 not in e1:
            e1.append(6)

        if 9 in e2 and 6 not in e2:
            e2.append(6)

        for a, b in pairs:
            if not ((a in e1 and b in e2) or (b in e1 and a in e2)):
                return False

        return True

    count = 0
    for c1 in itertools.combinations(d1, 6):
        for c2 in itertools.combinations(d2, 6):
            count += all_pairs_possible(c1, c2)

    return count // 2


with MyTimer() as t:
    print(solve())
