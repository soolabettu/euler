
/*
 * Project Euler 822
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>

void solve();

static int64_t pow_mod(int64_t base, int64_t exp, int64_t mod);

int main() {
    solve();
    return 0;
}

struct record {
	int num;
    int squarings;
	double base;
	
};


static
int find_smallest(struct record * arr, int n);

static
int find_smallest(struct record* arr, int n) {
    double min = ldexp(arr[0].base, arr[0].squarings);
    int idx = 0;
    for (int i = 1; i < n; i++) {
        double x = ldexp(arr[i].base, arr[i].squarings);
        if (x < min) {
            min = x;
            idx = i;
        }
    }

    // printf("idx = %d, arr[%d].num = %d, arr[%d].base = %f, arr[%d].exp = %d\n", idx, idx, arr[idx].num, idx, arr[idx].base, idx, arr[idx].exp);
    return idx;
}

void solve() {
    int upper_limit = 10;
    int n = upper_limit - 1;
    struct record *arr = (struct record*)malloc(n * sizeof(struct record));
    int64_t m = 100;
    int64_t mod = 1234567891;
    for (int i = 0; i < n ; i++) {
        arr[i].num = i + 2;
        arr[i].squarings = 0;
        arr[i].base = log(arr[i].num);
        // printf("arr[%d]->num = %d\n", i, arr[i].num);
        // printf("arr[%d]->base = %f\n", i, arr[i].base);
    }
    
    for (int i = 0; i < m; i++) {
        int idx = find_smallest(arr, n);
        arr[idx].squarings += 1;
        // printf("After operation %d: arr[%d] = %lld\n", i, idx, arr[idx]);
    }

    // for (int i = 0; i < n; i++) {
    //     printf("arr[%d].num = %d, arr[%d].exp = %d\n", i, arr[i].num, i, arr[i].exp);
    // }

    int64_t total = 0;
    for (int i = 0; i < n; i++) {
        int64_t e = pow_mod(2, arr[i].squarings, mod - 1);
        int64_t term = pow_mod(arr[i].num, e, mod);
        total = (total + term) % mod;
    }

    printf("Total: %lld\n", total);
    free(arr);
}


static int64_t pow_mod(int64_t base, int64_t exp, int64_t mod) {
      int64_t result = 1 % mod;
      base %= mod;

      while (exp > 0) {
          if (exp & 1) {
              result = (result * base) % mod;
          }
          base = (base * base) % mod;
          exp >>= 1;
      }

      return result;
}
