def solve():
    """Summation of maximal remainders for the binomial expression problem."""
    return sum(map(lambda a: (a + a % 2 - 2) * a, range(3, 1001)))


from mytimeit import MyTimer

with MyTimer() as t:
    print(solve())
