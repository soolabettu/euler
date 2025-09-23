def solve(limit):
    i = 0
    x = 1
    k = 0
    while i < limit:
        x *= 2
        k += 1
        if x > 1000:
            x /= 10

        if int(x) == 123:
            i += 1

    return k


from mytimeit import MyTimer

with MyTimer() as t:
    print(solve(678910))
