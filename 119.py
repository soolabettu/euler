from time import sleep


def solve():
    """Enumerate numbers equal to the sum of digits of their powers and list the results."""
    results = []
    num = 2

    while len(results) < 30:
        product = num
        for exp in range(1, 8):
            product *= num
            if sum(map(int, str(product))) == num:
                results.append((num, exp, product))
                print(num, exp, product)

        num += 1

    for i, entry in enumerate(sorted(results, key=lambda x: x[2])):
        print(i, entry)


from mytimeit import *

with MyTimer() as t:
    solve()
