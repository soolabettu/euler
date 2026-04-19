from collections import defaultdict
import sys
import time

inv_cnt = defaultdict(int)
char_to_digit = {}


def rank_characters(s):
    return {c: i for i, c in enumerate(sorted(set(s)), start=1)}


def inversion_count(s):
    global char_to_digit
    char_to_digit = rank_characters(s)
    digits = [char_to_digit[c] for c in s]
    inv_cnt.clear()
    inv_cnt.update(
        (digit, sum(d < digit for d in digits[i + 1 :]))
        for i, digit in enumerate(digits)
    )
    return digits, inv_cnt


def solve(values, digit, count, digit_totals):
    if digit == len(values) + 1:
        print(digit_totals[-1])
        return

    current_digit_moves = (digit - 1) * count
    less_than = inv_cnt[digit] if count % 2 == 0 else digit - inv_cnt[digit] - 1
    next_count = count + current_digit_moves + less_than
    return solve(values, digit + 1, next_count, digit_totals + [next_count])


if __name__ == "__main__":
    start = time.perf_counter()
    s = sys.argv[1] if len(sys.argv) > 1 else "NOWPICKBELFRYMATHS"
    digits, _ = inversion_count(s)
    solve(digits, 3, inv_cnt[2], [])
    elapsed = time.perf_counter() - start
    print(f"Elapsed: {elapsed:.6f}s", file=sys.stderr)
