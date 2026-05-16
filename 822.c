#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

enum {
    N = 10000,
    MOD = 1234567891
};

static const uint64_t M = 10000000000000000ULL;

static int cmp_u64(const void *lhs, const void *rhs) {
    uint64_t a = *(const uint64_t *)lhs;
    uint64_t b = *(const uint64_t *)rhs;
    return (a > b) - (a < b);
}

static uint64_t pow_mod(uint64_t base, uint64_t exp, uint64_t mod) {
    uint64_t result = 1 % mod;
    base %= mod;

    while (exp > 0) {
        if (exp & 1ULL) {
            result = (result * base) % mod;
        }
        base = (base * base) % mod;
        exp >>= 1;
    }

    return result;
}

static size_t find_min_index(const uint64_t *values, size_t len) {
    size_t min_index = 0;
    for (size_t i = 1; i < len; ++i) {
        if (values[i] < values[min_index]) {
            min_index = i;
        }
    }
    return min_index;
}

int main(void) {
    uint64_t *values = malloc((N - 1) * sizeof(*values));
    if (values == NULL) {
        fprintf(stderr, "allocation failed\n");
        return 1;
    }

    for (size_t i = 0; i < N - 1; ++i) {
        values[i] = i + 2;
    }

    uint64_t remaining = M;

    // Mirror the Python pre-balancing phase exactly.
    while (1) {
        size_t min_index = find_min_index(values, N - 1);
        uint64_t min_value = values[min_index];
        if (min_value > N / min_value) {
            break;
        }
        values[min_index] = min_value * min_value;
        --remaining;
    }

    qsort(values, N - 1, sizeof(*values), cmp_u64);

    uint64_t q = remaining / (N - 1);
    uint64_t r = remaining % (N - 1);

    uint64_t total = 0;
    for (size_t i = 0; i < N - 1; ++i) {
        uint64_t extra_squarings = q + (i < r ? 1ULL : 0ULL);
        uint64_t exponent = pow_mod(2, extra_squarings, MOD - 1);
        uint64_t term = pow_mod(values[i], exponent, MOD);
        total += term;
        total %= MOD;
    }

    printf("%" PRIu64 "\n", total);
    free(values);
    return 0;
}
