"""Project Euler Problem 845: https://projecteuler.net/problem=845"""

# Counts integers below 814 whose decimal representation contains no digit 1.


cnt = 0
for i in range(814):
    if "1" in str(i):
        continue
    cnt += 1

print(cnt)
