
#!/usr/bin/env python3

from mytimeit import *
import time
import math
from fractions import Fraction


def solve():

    f1 = Fraction(2, 1)
    ans = 0
    for i in range(1000):
        f2 = Fraction(2, 1)
        for j in range(i+1):
            f2 = f1 + 1/f2

        f2 = 1 + 1/f2
        ans += len(str(f2.numerator)) > len(str(f2.denominator))    
        
    print(ans)


if __name__ == "__main__":
    with MyTimer(solve) as timer:
        solve()
