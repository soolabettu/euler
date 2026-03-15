"""Project Euler Problem 323: https://projecteuler.net/problem=323"""

# Simulates repeated bitwise ORs of random 32-bit values until every bit has been set.


import random


# Examples
def solve():
    xprev = 0
    limit = 2**32 - 1
    yprev = random.randint(0, limit)
    i = 0
    while True:
        i += 1

        xnext = xprev | yprev
        if xnext == limit:
            break

        xprev = xnext
        yprev = random.randint(0, limit)

    # print(i)
    return i


from decimal import Decimal, getcontext


limit = 10**9
x = 0
for i in range(limit):
    x += solve()

y = x / limit

print(y)
# getcontext().prec = 10

# Example calculation
# result = Decimal(str(x)) / Decimal(str(limit))
# print(result)
