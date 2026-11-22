#include <math.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    const int bits = 32;
    const int places = 10;
    double partial = 0.0;

    for (int k = 0; ; ++k) {
        double p = ldexp(1.0, -k);  /* 2^(-k) */
        double term = k == 0 ? 1.0 : -expm1(bits * log1p(-p));
        partial += term;

        double tail_bound = bits * p;
        char lower[64];
        char upper[64];

        snprintf(lower, sizeof lower, "%.*f", places, partial);
        snprintf(upper, sizeof upper, "%.*f", places, partial + tail_bound);

        if (strcmp(lower, upper) == 0) {
            printf("E[T] rounded = %s\n", lower);
            printf("Stopped at k = %d\n", k);
            return 0;
        }
    }
}
