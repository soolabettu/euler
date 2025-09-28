#!/usr/bin/env python3
from collections import defaultdict, OrderedDict
from fractions import Fraction


def sum_distribution(num_dice: int, num_faces: int) -> OrderedDict:
    """
    Return an ordered dict {sum: count} for the sum of `num_dice` fair dice,
    each taking values 1..num_faces.
    Uses DP convolution, exact counts (integers).
    """
    dist = {0: 1}  # one way to get sum 0 (no dice)
    for _ in range(num_dice):
        new = defaultdict(int)
        for s, c in dist.items():
            for face in range(1, num_faces + 1):
                new[s + face] += c
        dist = new
    return OrderedDict(sorted(dist.items()))


def probability_player2_wins():
    # Player 1: six d6 (sums 6..36)
    dist_p1 = sum_distribution(num_dice=6, num_faces=6)
    total_p1 = 6**6

    # Player 2: nine d4 (sums 9..36)
    dist_p2 = sum_distribution(num_dice=9, num_faces=4)
    total_p2 = 4**9

    # Total joint outcomes
    total_joint = total_p1 * total_p2

    # Build cumulative distribution for Player 2 to speed comparisons
    # We need counts of P2 sums strictly greater than a given s1.
    sums_p2 = list(dist_p2.keys())
    max_sum = max(sums_p2)
    # Suffix cumulative counts: greater_counts[s] = sum_{t > s} dist_p2[t]
    greater_counts = {}
    running = 0
    # iterate descending
    for s in range(max_sum, -1, -1):
        greater_counts[s] = running
        if s in dist_p2:
            running += dist_p2[s]
    # Note: for any s1, P2_wins_count_given_s1 = greater_counts[s1]

    # Similarly, for ties we need dist_p2[s1] when s1 in P2's support
    p2_count = dist_p2  # alias

    # Accumulate joint counts
    joint_p2_wins = 0
    joint_ties = 0
    for s1, c1 in dist_p1.items():
        joint_p2_wins += c1 * greater_counts.get(s1, 0)
        joint_ties += c1 * p2_count.get(s1, 0)

    joint_p1_wins = total_joint - joint_p2_wins - joint_ties

    # Exact probabilities as reduced fractions
    p_p2_win = Fraction(joint_p2_wins, total_joint)
    p_tie = Fraction(joint_ties, total_joint)
    p_p1_win = Fraction(joint_p1_wins, total_joint)

    return {
        "p2_win": (p_p2_win, float(p_p2_win)),
        "tie": (p_tie, float(p_tie)),
        "p1_win": (p_p1_win, float(p_p1_win)),
    }


if __name__ == "__main__":
    result = probability_player2_wins()
    p2_frac, p2_float = result["p2_win"]
    tie_frac, tie_float = result["tie"]
    p1_frac, p1_float = result["p1_win"]

    print("Results for: Player 1 rolls six d6, Player 2 rolls nine d4")
    print("----------------------------------------------------------")
    print(f"Player 2 wins: {p2_frac}  ≈ {p2_float:.10f}")
    print(f"Tie:           {tie_frac}  ≈ {tie_float:.10f}")
    print(f"Player 1 wins: {p1_frac}  ≈ {p1_float:.10f}")
