import mytimeit
from math import isqrt


# Example
def solve():
    ans = set([1])
    i = 2
    flag = True
    while True:
        j = 1
        running_total = 0
        while True:
            x = i**j
            if len(str(x)) == j:
                ans.add(x)
            else:
                if j == 1:
                    flag = False
                break

            j += 1

        if not flag:
            break

        i += 1

    return len(ans)


with mytimeit.MyTimer() as t:
    print(solve())
