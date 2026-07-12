"""
Project Euler 706.

The task is to count n-digit positive integers for which the number of
contiguous substrings divisible by 3 is itself divisible by 3.  The final
answer is requested modulo 1_000_000_007.

Divisibility by 3 depends only on digit sums modulo 3, so the dynamic program
never needs to know the actual digits.  It only tracks prefix-sum remainders.

For a decimal string with prefix sums P[0], P[1], ..., P[k], the substring
from i + 1 through k has digit sum P[k] - P[i].  That substring is divisible
by 3 exactly when P[k] == P[i] (mod 3).  Therefore, when a new digit creates a
new prefix remainder r, the number of newly-created divisible substrings is
the number of earlier prefix boundaries with remainder r.

Only the final count of divisible substrings modulo 3 matters, because the
Euler condition is "count is divisible by 3".  For the same reason, the counts
of prior prefix remainders are also stored modulo 3: each step only adds one
of those counts into the substring total modulo 3.
"""

from collections import defaultdict

MOD = 1_000_000_007


def transition(state, digit):
    """Advance one digit-remainder from a compact DP state.

    Args:
        state: A 5-tuple/list `(p, c0, c1, c2, s)`.
            p:
                Current full-prefix digit-sum remainder modulo 3.
            c0, c1, c2:
                Counts, modulo 3, of previous prefix boundaries whose
                digit-sum remainders are 0, 1, and 2 respectively.  This
                includes the empty prefix before any digits are read.
            s:
                Current number of divisible substrings, modulo 3.
        digit: The next digit's remainder modulo 3.  The actual digit value is
            irrelevant to divisibility by 3.

    Returns:
        The updated state as a list.  Callers convert it to a tuple before
        using it as a dictionary key.
    """
    p, c0, c1, c2, s = state
    counts = [c0, c1, c2]

    # Remainder of the complete prefix after appending this digit.  This is
    # the P[k] value described in the module comment.
    new_p = (p + digit) % 3

    # Every previous prefix boundary with the same remainder forms one new
    # substring whose digit sum is 0 modulo 3.  Since only divisibility of the
    # total substring count by 3 matters, keep the running total modulo 3.
    new_s = (s + counts[new_p]) % 3

    # The newly-created prefix boundary becomes available for future
    # substrings.  Again, the exact count is unnecessary; its value modulo 3 is
    # enough for all future updates to s modulo 3.
    counts[new_p] = (counts[new_p] + 1) % 3

    return [new_p, counts[0], counts[1], counts[2], new_s]


def next_layer(dp, first_digit=False):
    """Build the DP table for the next decimal position.

    The DP dictionary maps compact states to the number of prefixes producing
    that state, modulo MOD.  Instead of iterating over all ten possible digits,
    the code groups them by remainder modulo 3:

        first digit, 1..9:  remainders 0, 1, 2 each occur 3 times
        later digits, 0..9: remainder 0 occurs 4 times; 1 and 2 occur 3 times

    `first_digit` prevents leading zeroes, because the problem asks for
    n-digit positive integers.
    """
    next_dp = defaultdict(int)

    if first_digit:
        # First digit: 1 through 9.  Each residue class has exactly three
        # representatives:
        #   0: 3, 6, 9
        #   1: 1, 4, 7
        #   2: 2, 5, 8
        remainder_multiplicity = [(0, 3), (1, 3), (2, 3)]
    else:
        # Later digits: 0 through 9.  Zero is now allowed, so residue 0 has
        # four representatives:
        #   0: 0, 3, 6, 9
        #   1: 1, 4, 7
        #   2: 2, 5, 8
        remainder_multiplicity = [(0, 4), (1, 3), (2, 3)]

    for state_tuple, number_count in dp.items():
        state = list(state_tuple)

        for digit_remainder, multiplicity in remainder_multiplicity:
            new_state = transition(state, digit_remainder)

            # Each residue transition represents `multiplicity` concrete
            # decimal digits.  Aggregate by compact state and reduce modulo
            # MOD to keep integer sizes bounded.
            next_dp[tuple(new_state)] += number_count * multiplicity
            next_dp[tuple(new_state)] %= MOD

    return next_dp


def solve(n):
    """Return the Euler 706 count for n-digit integers, modulo MOD."""
    # Before reading any digits:
    #   p = 0 because the empty prefix has digit sum 0
    #   c0 = 1 because that empty prefix is one boundary with remainder 0
    #   c1 = c2 = 0 because no other prefix remainders exist yet
    #   s = 0 because no non-empty substrings exist yet
    dp = {
        (0, 1, 0, 0, 0): 1
    }

    # Append one digit at a time.  There are at most
    #   3 choices for p
    #   3 choices each for c0, c1, c2
    #   3 choices for s
    # so the state space is capped at 3**5 = 243 states, making n = 10**5
    # cheap to process.
    for position in range(n):
        dp = next_layer(dp, first_digit=(position == 0))

    # Accept exactly those states where the number of divisible substrings is
    # 0 modulo 3.
    answer = sum(
        count
        for state, count in dp.items()
        if state[4] == 0
    )

    return answer % MOD


print(solve(10**5))
