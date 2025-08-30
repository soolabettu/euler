import mytimeit
from itertools import permutations


# Example
def solve(N):
    cube_dict = {i: "".join(sorted(str(i**3))) for i in range(N)}
    value_counts = {}
    for k, v in cube_dict.items():
        value_counts.setdefault(v, [0, []])
        value_counts[v][0] += 1
        value_counts[v][1].append(k)
    for k, v in sorted(value_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(k, v)


with mytimeit.MyTimer() as t:
    print(solve(10000))
