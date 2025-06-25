from mytimeit import *


def solve(limit):
    i = 1
    p_nums = []
    while limit > i:
        x = i * (3 * i - 1) // 2
        i += 1
        p_nums.append(x)

    candidates = []
    for i in p_nums:
        for j in p_nums:
            if i >= j:
                continue
            if i + j > p_nums[-1]:
                break
            if i + j in p_nums and abs(i - j) in p_nums:
                print(i, j, abs(i - j), i + j)

    return p_nums


if __name__ == "__main__":
    with MyTimer(solve) as timer:
        solve(3000)
