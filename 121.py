from fractions import Fraction
import mytimeit


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


with mytimeit.MyTimer() as t:
    # ---- fifteen-turn game ----
    p15 = solve(15)  # exact Fraction
    p15_float = float(p15)  # ≈ 0.0004406

    entry_fee = 1.0  # dollars
    payout_break_even = entry_fee / p15_float

    print(f"Probability of winning in 15 turns : {p15} ≈ {p15_float:.6e}")
    print(f"Break-even payout per win          : ${payout_break_even:,.2f}")
