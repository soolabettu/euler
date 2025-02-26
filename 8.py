#!/usr/bin/env python3

var = input()
candidate = ""
ans = 0
for i in var:
    candidate += i
    if i == "0":
        candidate = ""

    if len(candidate) == 13:
        temp_ans = 1
        for z in candidate:
            temp_ans = temp_ans * int(z)

        ans = max(ans, temp_ans)
        candidate = candidate[1:]


print(ans)
