/* Project Euler Problem 650: https://projecteuler.net/problem=650 */
// Builds prime-exponent tables in C and accumulates the divisor-sum sequence modulo 1e9+7.

#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

#define MOD 1000000007LL

/* Computes (base^exp) mod MOD using binary exponentiation.
 * Runs in O(log exp) time by squaring the base and consuming bits of exp.
 * Assumes exp >= 0.
 */
static int64_t mod_pow(int64_t base, int64_t exp) {
    int64_t result = 1;
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

static int* build_spf(int limit) {
    int* spf = (int*)malloc((size_t)(limit + 1) * sizeof(int));
    if (spf == NULL) {
        return NULL;
    }

    for (int i = 0; i <= limit; ++i) {
        spf[i] = i;
    }
    if (limit >= 1) {
        spf[1] = 1;
    }

    int root = (int)sqrt((double)limit);
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

/* Fills prime_vals/prime_cnts with factorization pairs for x using spf.
 * Returns number of (prime, exponent) pairs written.
 */
static int factorize_with_spf(int x, const int* spf, int* prime_vals, int* prime_cnts) {
    int out_len = 0;
    while (x > 1) {
        int p = spf[x];
        int c = 0;
        while (x % p == 0) {
            x /= p;
            ++c;
        }
        prime_vals[out_len] = p;
        prime_cnts[out_len] = c;
        ++out_len;
    }
    return out_len;
}

static int64_t solve(int n) {
    if (n <= 0) {
        return 0;
    }

    int* spf = build_spf(n);
    if (spf == NULL) {
        fprintf(stderr, "Failed to allocate spf\n");
        return -1;
    }

    int* primes = (int*)malloc((size_t)(n + 1) * sizeof(int));
    int* idx_of = (int*)malloc((size_t)(n + 1) * sizeof(int));
    int64_t* a = NULL;
    int64_t* f = NULL;
    int64_t* inv_pm1 = NULL;

    if (primes == NULL || idx_of == NULL) {
        free(spf);
        free(primes);
        free(idx_of);
        fprintf(stderr, "Failed to allocate prime metadata\n");
        return -1;
    }

    for (int i = 0; i <= n; ++i) {
        idx_of[i] = -1;
    }

    int m = 0;
    for (int i = 2; i <= n; ++i) {
        if (spf[i] == i) {
            primes[m] = i;
            idx_of[i] = m;
            ++m;
        }
    }

    a = (int64_t*)calloc((size_t)m, sizeof(int64_t));
    f = (int64_t*)calloc((size_t)m, sizeof(int64_t));
    inv_pm1 = (int64_t*)calloc((size_t)m, sizeof(int64_t));
    if (a == NULL || f == NULL || inv_pm1 == NULL) {
        free(spf);
        free(primes);
        free(idx_of);
        free(a);
        free(f);
        free(inv_pm1);
        fprintf(stderr, "Failed to allocate state arrays\n");
        return -1;
    }

    for (int i = 0; i < m; ++i) {
        inv_pm1[i] = mod_pow((int64_t)primes[i] - 1, MOD - 2);
    }

    int64_t total = 0;
    int active = 0;

    int factor_primes[64];
    int factor_counts[64];

    for (int k = 1; k <= n; ++k) {
        if (k >= 2 && spf[k] == k) {
            ++active;
        }

        int factor_len = factorize_with_spf(k, spf, factor_primes, factor_counts);
        for (int i = 0; i < factor_len; ++i) {
            int p = factor_primes[i];
            int v = factor_counts[i];
            int idx = idx_of[p];
            a[idx] += v;
        }

        int64_t d_k = 1;
        int64_t kp1 = (int64_t)k + 1;

        for (int i = 0; i < active; ++i) {
            int64_t ai = a[i];
            int64_t fi = f[i] + ai;
            f[i] = fi;
            int64_t e = kp1 * ai - 2 * fi;
            if (e != 0) {
                int64_t p = primes[i];
                int64_t term = (mod_pow(p, e + 1) - 1 + MOD) % MOD;
                term = (term * inv_pm1[i]) % MOD;
                d_k = (d_k * term) % MOD;
            }
        }

        total += d_k;
        if (total >= MOD) {
            total -= MOD;
        }
    }

    free(spf);
    free(primes);
    free(idx_of);
    free(a);
    free(f);
    free(inv_pm1);

    return total;
}

int main(void) {
    struct timeval start;
    struct timeval end;
    gettimeofday(&start, NULL);
    int64_t ans = solve(20000);
    gettimeofday(&end, NULL);

    double elapsed = (double)(end.tv_sec - start.tv_sec) +
                     (double)(end.tv_usec - start.tv_usec) / 1000000.0;

    printf("%lld\n", (long long)ans);
    printf("Elapsed: %.6f s\n", elapsed);
    return 0;
}
