"""Project Euler Problem 56: https://projecteuler.net/problem=56"""

# Searches a^b for 1 <= a,b < 100 and keeps the maximum digital sum.


ans = 0
for i in range(1, 100):
    for j in range(1, 100):
        ans = max(ans, sum([int(i) for i in str(i**j)]))

print(ans)
