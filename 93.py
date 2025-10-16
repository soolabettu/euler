# Evaluate all full-binary expressions over operands a=1, b=2, c=3, d=4
# using operators {+, -, *, /}, with exact rational arithmetic.
from itertools import permutations
from fractions import Fraction
from collections import Counter
import pandas as pd

# from caas_jupyter_tools import display_dataframe_to_user


def shapes(n):
    """Yield all full-binary tree shapes with n leaves."""
    if n == 1:
        yield ("leaf",)
        return
    for k in range(1, n):
        for L in shapes(k):
            for R in shapes(n - k):
                yield (None, L, R)


def assign_ops(shape, ops):
    """Attach operators from ops to each internal node of the tree shape."""
    if shape[0] == "leaf":
        yield ("leaf",)
        return
    _, L, R = shape
    for l in assign_ops(L, ops):
        for r in assign_ops(R, ops):
            for op in ops:
                yield (op, l, r)


def fill_leaves(tree, values):
    """Populate the leaves of the operator tree with the provided values."""
    it = iter(values)

    def _fill(t):
        """Return a new tree with leaves replaced by successive values."""
        if t[0] == "leaf":
            return ("leaf", next(it))
        op, L, R = t
        return (op, _fill(L), _fill(R))

    return _fill(tree)


def eval_tree(t):
    """Evaluate the expression tree using Fraction arithmetic, guarding against division by zero."""
    if t[0] == "leaf":
        return Fraction(t[1], 1)
    op, L, R = t
    lv = eval_tree(L)
    rv = eval_tree(R)
    if op == "+":
        return lv + rv
    elif op == "-":
        return lv - rv
    elif op == "*":
        return lv * rv
    elif op == "/":
        if rv == 0:
            return None
        return lv / rv


def to_infix(t):
    """Render the expression tree as a parenthesized infix string."""
    if t[0] == "leaf":
        return str(t[1])
    op, L, R = t
    return f"({to_infix(L)} {op} {to_infix(R)})"


from itertools import combinations


def choose_4_from_9(digits=None):
    """
    Return all unordered ways to choose 4 distinct digits from 9 digits.
    By default uses digits 1..9. Order does not matter.
    """
    if digits is None:
        digits = list(range(1, 10))  # 1..9
    if len(digits) != 9:
        raise ValueError("Provide exactly 9 digits.")
    return list(combinations(digits, 4))


def longest_consecutive_sorted(nums):
    """Assumes nums is sorted. Returns length of the longest run of consecutive ints."""
    if not nums:
        return 0
    best = curr = 1
    prev = nums[0]
    for x in nums[1:]:
        if x == prev:  # duplicate, ignore
            continue
        if x == prev + 1:  # extends the streak
            curr += 1
        else:  # streak breaks
            curr = 1
        best = max(best, curr)
        prev = x
    return best


def solve():
    """Determine the 4-digit set producing the longest run of consecutive positive integers."""
    combos = choose_4_from_9()  # default: digits 1..9
    ans = 0
    longest = []
    # print(f"Total combinations: {len(combos)}")  # should be 9 choose 4 = 126
    with open("93.txt", "w") as f:
        for c in combos:
            operands = list(c)

            ops = ["+", "-", "*", "/"]
            # operands = [1, 2, 3, 4]

            values = []
            examples = {}
            count_total = 0
            count_valid = 0

            for shp in shapes(len(operands)):
                for with_ops in assign_ops(shp, ops):
                    for perm in permutations(operands):
                        count_total += 1
                        filled = fill_leaves(with_ops, perm)
                        val = eval_tree(filled)
                        if val is None:
                            continue
                        count_valid += 1
                        values.append(val)
                        if val not in examples:
                            examples[val] = to_infix(filled)

            freq = Counter(values)

            # Filter: positive integers only
            pos_ints = [
                v.numerator
                for v in set(values)
                if v.denominator == 1 and v.numerator > 0
            ]
            pos_ints_sorted = sorted(pos_ints, key=lambda x: x.numerator)
            temp_ans = longest_consecutive_sorted(pos_ints_sorted)
            if temp_ans > ans:
                ans = temp_ans
                longest = operands

            f.write(f"{operands} = {pos_ints_sorted}\n")

    print(f"Answer: {ans}")
    print(f"Longest consecutive: {longest}")


from mytimeit import *

with MyTimer() as t:
    solve()
