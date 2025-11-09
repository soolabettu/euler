#include<stdio.h>
#include<string.h>
#include <stdint.h>
#include <inttypes.h>


static
int explore(int i, int n, char *str, int target);

void solve();

double measure_time(void (*func)(void));

// Entry point: measures runtime of solve() and prints elapsed wall-clock seconds.
int main() {
    double elapsed = measure_time(solve);
    printf("Time taken: %.6f seconds\n", elapsed);
    return 0;
}

#include<time.h>

/**
 * solve - Enumerate squares whose digit splits sum to the square root.
 *
 * Iterates over candidate roots, skips impossible cases via modulo 9,
 * and uses explore() to check if the square's digits can be partitioned
 * into chunks summing to the root. Accumulates and prints qualifying squares.
 */
void solve() {
        char str[1024] = {'\0'};
        long long cnt = 0;
        for (uint64_t i = 9;(long long)i * i <= 1000000000000LL;i++) {
            uint64_t square = i * i;
            if (i % 9 != square % 9) 
                continue;
            int n = sprintf(str, "%" PRIu64, square);
            if (explore(-1, n, str, i) == 1) {
                cnt += square;
                printf("%lld %s\n", i, str);
            }
        }

        printf("%lld\n", cnt);
}

/**
 * measure_time - Helper to measure execution time of a void(void) function.
 * @func: Target function whose duration should be reported.
 *
 * Returns the elapsed seconds using the process clock.
 */
double measure_time(void (*func)(void)) {
    clock_t start = clock();
    func();
    clock_t end = clock();

    // CLOCKS_PER_SEC gives number of clock ticks per second
    return (double)(end - start) / CLOCKS_PER_SEC;
}

/**
 * explore - Recursively test whether digit partitions sum to target.
 * @i:      Current index within the digit string.
 * @n:      Length of the digit string.
 * @str:    Null-terminated string representation of the square.
 * @target: Remaining value the partitions must sum to.
 *
 * Returns 1 if a valid partition exists, otherwise 0.
 */
static int explore(int i , int n, char *str, int target) {
    if (target < 0) 
        return 0;

    if (target == 0 && i == n - 1) 
        return 1;

    if (i >= n)
        return 0;

    int l = i + 1;
    char temp[1024] = {'\0'};
    int k = 0;
    for (int j = i + 1; j < n; j++) {
        int chunk = 0;
        while (l <= j) {
            temp[k] = str[l];
            k++;
            l++;
        }

        temp[k] = '\0';
        sscanf(temp, "%d", &chunk);

        if (explore(j, n, str, target - chunk) == 1) return 1;
    }

    return 0;
}
