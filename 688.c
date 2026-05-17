
#include<stdio.h>
#include<time.h>

#define MOD 1000000007

/*
 * Euler 688 notes
 *
 * For a fixed number of piles k and smallest pile m, the least possible
 * total number of plates is the consecutive arrangement:
 *
 *     m + (m + 1) + ... + (m + k - 1)
 *       = k*m + k*(k - 1)/2
 *
 * For every total <= n that can support this arrangement, m contributes to
 * the answer.  This code sums by k first, then sums all valid m for that k
 * with arithmetic series instead of iterating over every total.
 */

static long long mod_mul(long long a, long long b) {
    /* Products can exceed int64 before the modulus when n is 10^16. */
    return (long long)((__int128)(a % MOD) * (b % MOD) % MOD);
}

static long long tri_mod(long long n) {
    /* 1 + 2 + ... + n, reduced modulo MOD. */
    return (long long)((__int128)n * (n + 1) / 2 % MOD);
}

static long long solve(long long n) {
    long long total = 0;
    for (long long k = 1;;k++) {
        /*
         * k piles are possible only if the minimum arrangement with m = 1,
         * namely 1 + 2 + ... + k, fits within n.
         */
        if (k * (k + 1) / 2 > n) {
            break;
        }

        /*
         * Largest smallest-pile value m such that
         *
         *     k*m + k*(k - 1)/2 <= n
         */
        long long upper_limit = (n - k * (k - 1) / 2) / k;

        /*
         * For m = 1..upper_limit-1, there is a full block of k totals that
         * include this m, so the contribution is:
         *
         *     k * (1 + 2 + ... + upper_limit-1)
         */
        long long upper_limit_1 = upper_limit - 1;
        total = (total + mod_mul(tri_mod(upper_limit_1), k)) % MOD;

        /*
         * The final m = upper_limit may have only a partial block, depending
         * on how close its minimum arrangement is to n.
         */
        long long last_block = upper_limit + k - 1;
        last_block = (long long)((__int128)last_block * (last_block + 1) / 2
                - (__int128)upper_limit * (upper_limit - 1) / 2);

        /*
         * Add the final m once for its base arrangement, then once more for
         * each extra total after last_block that still stays <= n.
         */
        total = (total + upper_limit % MOD) % MOD + (n - last_block) * upper_limit % MOD;
    }

    return total;
}

int main(){
    clock_t start = clock();
    long long total = 0;
    long long n = 10000000000000000;
    total = solve(n);
    printf("Total: %lld\n", total);
    printf("Elapsed: %.6f seconds\n", (double)(clock() - start) / CLOCKS_PER_SEC);
    return 0;
}
