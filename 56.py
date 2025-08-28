import mytimeit

with mytimeit.MyTimer() as t:
    ans = 0
    for i in range(1, 100):
        for j in range(1, 100):
            ans = max(ans, sum([int(i) for i in str(i**j)]))

    print(ans)
