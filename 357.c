
#include<stdio.h>
#include<time.h>


static void solve(long long limit);

int primes[100000001] = {0};
int ans[100000001] = {0};

int main(void) {
    clock_t start, end;
    double cpu_time_used;

    start = clock();

    solve(100000000);

    end = clock();

    cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;

    printf("Time taken: %.6f seconds\n", cpu_time_used);

    return 0;
	return 0;
}


static void solve(long long limit) {
    int m = 10000;
    primes[0] = 0;
    primes[1] = 1;
    primes[2] = 0;

    for (int i = 2;i <= m;i++) {
        for (int j = 2;i * j <= limit;j++) {
            primes[i * j] = 1;
        }
    }

    for (int i = 1;i <= m;++i) {
        for (int j = 1;i * j <= limit;j++) {
            if (primes[i+j] == 1) {
                ans[i*j] = 1;
            }
        }
    }

    long long result = 0;

    for (int i = 1;i <= limit;i++) {
        if (ans[i] == 0) {
            result += i;
        }
    }

    printf("%lld\n", result);
}
