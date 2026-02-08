# Example:
def solve(num, target):
    n = int(bin(target), 2)
    bits = [1 << i for i in range(n.bit_length()) if n >> i & 1]
    s = 0
    ans = 0
    for b in bits:
        s += b
        ans += num - s
    print(num + ans)


from mytimeit import *

with MyTimer() as t:
    solve(10**17, 10**17 - 9**17)
