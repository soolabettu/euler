"""Project Euler Problem 62: https://projecteuler.net/problem=62"""

# Groups cubes by sorted digits to find families of cube permutations.

from itertools import permutations


# Example
def solve(N):
    """Group cubes below N by digit permutations and display the most common signatures."""
    cube_dict = {i: "".join(sorted(str(i**3))) for i in range(N)}
    value_counts = {}
    for k, v in cube_dict.items():
        value_counts.setdefault(v, [0, []])
        value_counts[v][0] += 1
        value_counts[v][1].append(k)
    for k, v in sorted(value_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(k, v)


print(solve(10000))
