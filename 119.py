from time import sleep


def solve():
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
