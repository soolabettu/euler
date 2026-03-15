/* Project Euler Problem 650: https://projecteuler.net/problem=650 */
// Builds prime-exponent tables and accumulates the divisor-sum sequence modulo 1e9+7.

#include <chrono>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <unordered_map>
#include <utility>
#include <vector>

namespace {

constexpr std::int64_t MOD = 1'000'000'007LL;

// Computes (base^exp) mod MOD using binary exponentiation.
// Runs in O(log exp) time by squaring the base and consuming bits of exp.
// Assumes exp >= 0.
std::int64_t mod_pow(std::int64_t base, std::int64_t exp) {
    std::int64_t result = 1;
    base %= MOD;
    while (exp > 0) {
        if (exp & 1LL) {
            result = (result * base) % MOD;
        }
        base = (base * base) % MOD;
        exp >>= 1LL;
    }
    return result;
}

std::vector<int> build_spf(int limit) {
    std::vector<int> spf(limit + 1);
    for (int i = 0; i <= limit; ++i) {
        spf[i] = i;
    }
    if (limit >= 1) {
        spf[1] = 1;
    }

    int root = static_cast<int>(std::sqrt(limit));
    for (int i = 2; i <= root; ++i) {
        if (spf[i] == i) {
            for (int j = i * i; j <= limit; j += i) {
                if (spf[j] == j) {
                    spf[j] = i;
                }
            }
        }
    }
    return spf;
}

std::vector<std::pair<int, int>> factorize_with_spf(int x, const std::vector<int>& spf) {
    std::vector<std::pair<int, int>> out;
    while (x > 1) {
        int p = spf[x];
        int c = 0;
        while (x % p == 0) {
            x /= p;
            ++c;
        }
        out.push_back({p, c});
    }
    return out;
}

std::int64_t solve(int n) {
    if (n <= 0) {
        return 0;
    }

    std::vector<int> spf = build_spf(n);
    std::vector<int> primes;
    primes.reserve(n / std::max(1.0, std::log(n)));
    for (int i = 2; i <= n; ++i) {
        if (spf[i] == i) {
            primes.push_back(i);
        }
    }

    std::unordered_map<int, int> idx_of;
    idx_of.reserve(primes.size() * 2);
    for (int i = 0; i < static_cast<int>(primes.size()); ++i) {
        idx_of[primes[i]] = i;
    }

    int m = static_cast<int>(primes.size());
    std::vector<std::int64_t> a(m, 0);
    std::vector<std::int64_t> f(m, 0);
    std::vector<std::int64_t> inv_pm1(m, 0);
    for (int i = 0; i < m; ++i) {
        inv_pm1[i] = mod_pow(primes[i] - 1, MOD - 2);
    }

    std::int64_t total = 0;
    int active = 0;

    for (int k = 1; k <= n; ++k) {
        if (k >= 2 && spf[k] == k) {
            ++active;
        }

        for (const auto& [p, v] : factorize_with_spf(k, spf)) {
            a[idx_of[p]] += v;
        }

        std::int64_t d_k = 1;
        std::int64_t kp1 = static_cast<std::int64_t>(k) + 1;

        for (int i = 0; i < active; ++i) {
            std::int64_t ai = a[i];
            std::int64_t fi = f[i] + ai;
            f[i] = fi;
            std::int64_t e = kp1 * ai - 2 * fi;
            if (e != 0) {
                std::int64_t p = primes[i];
                std::int64_t term = (mod_pow(p, e + 1) - 1 + MOD) % MOD;
                term = (term * inv_pm1[i]) % MOD;
                d_k = (d_k * term) % MOD;
            }
        }

        total += d_k;
        if (total >= MOD) {
            total -= MOD;
        }
    }

    return total;
}

}  // namespace

int main() {
    const auto start = std::chrono::steady_clock::now();
    const auto ans = solve(20000);
    const auto end = std::chrono::steady_clock::now();
    const std::chrono::duration<double> elapsed = end - start;

    std::cout << ans << '\n';
    std::cout << "Elapsed: " << elapsed.count() << " s\n";
    return 0;
}
