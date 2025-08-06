from fractions import Fraction


def solve(turns):

    dp = [[Fraction(0) for _ in range(turns + 1)] for _ in range(turns + 1)]
    dp[0][0] = Fraction(1)

    for k in range(1, turns + 1):
        p_black = Fraction(1, k + 1)  # P(black on turn k)
        p_red = Fraction(k, k + 1)  # P(red   on turn k)
        for b in range(0, k + 1):
            if b == 0:
                dp[k][b] = p_black
            else:
                dp[k][b] = dp[k - 1][b] * p_red + dp[k - 1][b - 1] * p_black

    return sum(dp[-1][b] for b in range(turns + 1) if b > turns - b)


def win_prob(n_turns: int) -> Fraction:
    """
    Return the exact probability of drawing more blacks than reds
    after n_turns, with replacement and one extra red added each turn.
    """
    # dp[b] = P(exactly b blacks after the processed turns)
    dp = [Fraction(1)] + [Fraction(0)] * n_turns
    # print(dp)

    for k in range(1, n_turns + 1):
        p_black = Fraction(1, k + 1)  # P(black on turn k)
        p_red = Fraction(k, k + 1)  # P(red   on turn k)
        new_dp = [Fraction(0)] * (n_turns + 1)

        for b in range(k):  # blacks so far cannot exceed k-1
            new_dp[b] += dp[b] * p_red  # draw red
            new_dp[b + 1] += dp[b] * p_black  # draw black
        dp = new_dp
        print(k, dp)

    print(dp)

    return sum(dp[b] for b in range(n_turns + 1) if b > n_turns - b)


# ---- fifteen-turn game ----
p15 = solve(15)  # exact Fraction
p15_float = float(p15)  # ≈ 0.0004406

entry_fee = 1.0  # dollars
payout_break_even = entry_fee / p15_float

print(f"Probability of winning in 15 turns : {p15} ≈ {p15_float:.6e}")
print(f"Break-even payout per win          : ${payout_break_even:,.2f}")
