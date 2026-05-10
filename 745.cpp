#include <chrono>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <vector>

using std::int64_t;

// Project Euler 745 scratch implementation.
//
// The target quantity is
//
//     S(n) = sum_{m=1..n} g(m)
//
// where g(m) is the largest perfect-square divisor of m.
//
// For each k >= 1, the numbers with largest square divisor exactly k^2 are
// precisely the values m = k^2 * s where s is squarefree. That lets us write
// the answer as
//
//     S(n) = sum_{k^2 <= n} k^2 * Q(floor(n / k^2))
//
// where Q(x) is the number of squarefree integers up to x.
//
// The squarefree counting step is handled with Möbius inversion:
//
//     Q(x) = sum_{d^2 <= x} mu(d) * floor(x / d^2)
//
// This file is a direct C++ translation of the same Möbius-based experiment in
// 745.py. It is much better than brute-force marking of multiples, while still
// leaving room for further algorithmic optimization at very large scales.

std::vector<int> generate_mobius(int n) {
    // Compute mu(0..n) with a linear sieve.
    //
    // mu(d) is:
    // -  1 when d has an even number of distinct prime factors
    // - -1 when d has an odd number of distinct prime factors
    // -  0 when d is divisible by any square > 1
    std::vector<int> mu(n + 1, 0);
    std::vector<bool> is_prime(n + 1, true);
    std::vector<int> primes;

    mu[1] = 1;
    if (n >= 0) {
        is_prime[0] = false;
    }
    if (n >= 1) {
        is_prime[1] = false;
    }

    for (int i = 2; i <= n; ++i) {
        if (is_prime[i]) {
            primes.push_back(i);
            mu[i] = -1;
        }

        for (int p : primes) {
            if (static_cast<int64_t>(i) * p > n) {
                break;
            }
            is_prime[i * p] = false;

            if (i % p == 0) {
                mu[i * p] = 0;
                break;
            } else {
                mu[i * p] = -mu[i];
            }
        }
    }

    return mu;
}

int64_t solve(int64_t n) {
    // Evaluate
    //
    //   sum_{k^2 <= n} k^2 * Q(floor(n / k^2))
    //
    // directly, where Q is the squarefree-counting function derived from the
    // Möbius formula above.
    static constexpr int64_t mod = 1000000007LL;
    const int64_t root = static_cast<int64_t>(std::sqrt(static_cast<long double>(n)));
    const std::vector<int> mu = generate_mobius(static_cast<int>(root));
    int64_t total = 0;

    for (int64_t k = 1; k <= root; ++k) {
        int64_t d = 1;
        int64_t cnt = 0;
        while (true) {
            const int64_t kd = k * d;
            const int64_t denom = kd * kd;
            // floor(n / (k^2 * d^2)) counts how many multiples of d^2 remain
            // after removing the k^2 factor.
            const int64_t val = n / denom;
            if (val < 1) {
                break;
            }
            cnt += static_cast<int64_t>(mu[static_cast<std::size_t>(d)]) * val;
            ++d;
        }

        // Every value in this class contributes k^2 to the final sum.
        total = (total + ((cnt % mod + mod) % mod) * ((k * k) % mod)) % mod;
    }

    return total;
}

int main() {
    // Large input used for performance experiments.
    const auto start = std::chrono::steady_clock::now();
    const int64_t n = 100000000000000LL;
    const int64_t total = solve(n);
    const auto end = std::chrono::steady_clock::now();
    const std::chrono::duration<double> elapsed = end - start;
    std::cout << "Total: " << total << '\n';
    std::cout << "Time: " << elapsed.count() << " seconds\n";
    return 0;
}
