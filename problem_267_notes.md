# Project Euler 267: logarithms and the wins threshold

Notes from the discussion on 2026-09-13.

## What the wealth formula represents

Starting with one pound, choose a fixed betting proportion `f` for all 1,000
coin tosses. A win multiplies the current wealth by `1 + 2f`, and a loss
multiplies it by `1 - f`.

After `w` wins and `1000 - w` losses, final wealth is

$$
W(w,f)=(1+2f)^w(1-f)^{1000-w}.
$$

This is wealth, not a probability. The order of the wins and losses does not
affect the product. The goal is to choose `f` to maximize the probability of
finishing with at least one billion pounds.

## Why take logarithms?

The number of wins `w` appears in the exponents, which makes it difficult to
isolate. Logarithms turn those exponents into ordinary multiplication.

The two useful rules, for positive `a` and `b`, are

$$
\ln(a^w)=w\ln(a),
\qquad
\ln(ab)=\ln(a)+\ln(b).
$$

For `0 < f < 1`, taking logarithms of the wealth formula gives

$$
\ln W(w,f)=w\ln(1+2f)+(1000-w)\ln(1-f).
$$

Expanding and collecting the terms containing `w` gives

$$
\ln W(w,f)
=1000\ln(1-f)
+w\bigl[\ln(1+2f)-\ln(1-f)\bigr].
$$

For a fixed `f`, everything except `w` is a constant. The equation now has
the simple form

$$
\text{log wealth}=\text{constant}+w\times\text{constant}.
$$

This makes solving for the required number of wins straightforward.

## Why the target condition is preserved

Logarithms are increasing functions. Therefore, taking logarithms preserves
the comparison with the target:

$$
W(w,f)\ge 10^9
\quad\Longleftrightarrow\quad
\ln W(w,f)\ge\ln(10^9).
$$

Taking logarithms is an exact algebraic transformation, not an approximation.

Substituting the expression for log wealth and rearranging gives

$$
w\bigl[\ln(1+2f)-\ln(1-f)\bigr]
\ge\ln(10^9)-1000\ln(1-f).
$$

For `0 < f < 1`, the quantity in square brackets is positive, so dividing by
it preserves the inequality:

$$
w\ge
\frac{\ln(10^9)-1000\ln(1-f)}
{\ln(1+2f)-\ln(1-f)}.
$$

Call the expression on the right the continuous wins threshold `w(f)`.
Actual wins are integers, so the minimum required win count is

$$
w_{\min}(f)=\lceil w(f)\rceil.
$$

The inequality points this way because the objective is to reach **at least**
the target. The number of wins must be at least the threshold.

Any logarithm base gives the same threshold if used consistently. With base-10
logarithms, `log10(10^9) = 9`. With natural logarithms, use `ln(10^9)`, not `9`.
The logarithmic formula excludes the endpoints `f = 0` and `f = 1`; these must
be handled directly using the original wealth rules.

## How derivatives enter

Once the threshold is written as a function of `f`, finding the best continuous
threshold becomes a problem of finding the lowest point of a curve.

The derivative measures how the threshold changes when `f` changes slightly:

$$
w'(f)=\lim_{h\to0}\frac{w(f+h)-w(f)}{h}.
$$

- A negative derivative means increasing `f` reduces the required wins.
- A positive derivative means increasing `f` increases the required wins.
- At a smooth interior minimum, the tangent is horizontal and the derivative
  is zero. A change from negative to positive identifies a minimum.

The value that becomes zero is the slope, not the number of required wins.
Graphing or searching increasingly fine values of `f` can also locate the
minimum; differentiation provides a precise way to identify it.

Bisection searches for the zero of the derivative by repeatedly halving an
interval containing the minimum. For this curve, the derivative changes sign
from negative to positive exactly once. A positive derivative at the midpoint
means retain the left half; a negative derivative means retain the right half.

## From the threshold to a probability

There are `C(1000, w)` sequences containing exactly `w` wins, and all `2^1000`
coin-toss sequences are equally likely. For a fixed proportion, sum over all
win counts that reach the target:

$$
\Pr(\text{final wealth}\ge10^9)
=\frac{1}{2^{1000}}
\sum_{w=w_{\min}(f)}^{1000}\binom{1000}{w}.
$$

If the threshold exceeds 1,000 wins, success is impossible and the sum is empty.

A smaller integer threshold gives a larger success probability. Different
proportions can have the same integer threshold and therefore the same
probability, even when their continuous thresholds differ.

Logarithms let us isolate the wins threshold; derivatives help locate its
minimum; the binomial sum converts the required win count into a probability.
