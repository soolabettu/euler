"""Project Euler Problem 872: https://projecteuler.net/problem=872"""

# Uses the target's set bits to accumulate the path sum in the problem's subtraction tree.


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


solve(10**17, 10**17 - 9**17)
