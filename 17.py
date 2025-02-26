#!/usr/bin/env python3


import math
import time


start = time.time()
ans = 0
my_dict = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
    20: "twenty",
}

tens_dict = {
    1: 3,
    2: 6,
    3: 6,
    4: 5,
    5: 5,
    6: 5,
    7: 7,
    8: 6,
    9: 6,
}


for i in range(1, 1001):
    if i == 1000:
        ans += 11
    elif i % 100 == 0:
        ans += len(my_dict[i // 100]) + len("hundred")
    else:
        if i // 100 > 0:
            ans += len(my_dict[i // 100]) + len("hundredand")
        y = i % 100
        if y < 20:
            ans += len(my_dict[y])
        else:
            if y // 10 > 0:
                ans += tens_dict[y // 10]
            if y % 10 > 0:
                ans += len(my_dict[y % 10])


print(ans)

end = time.time()
elapsed = end - start

print(f"Program took {elapsed:.2f} seconds to run")
