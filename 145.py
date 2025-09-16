
# Example:
def solve(limit):
    cnt = 0
    for i in range(11, limit):
        if int(str(i)[0])%2 == int(str(i)[-1]):
            continue

        rev = str(i)[::-1] 
        if rev[0] == "0":
            continue

        if any(c in '02468' for c in str(i + int(rev))):
            continue

        cnt += 1
    print(cnt)

from mytimeit import *

with MyTimer() as t:
    solve(10**9)
    


# Answer: Efficient solution by hand.
# nine digits       none
# eight digits    540000
# seven digits     50000
# six digits       18000
# five digits       none
# four digits        600
# three digits       100
# two digits          20
#                 ______
# Total           608720