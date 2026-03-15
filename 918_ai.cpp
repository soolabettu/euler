// Uses multiprecision recurrences to evaluate the custom sequence exactly for huge indices.

#include <iostream>
#include <stdexcept>
#include <boost/multiprecision/cpp_int.hpp>

using boost::multiprecision::cpp_int;

// Fast MSB index for uint64_t (works for n>=1)
static int msb_index(uint64_t n) {
#if defined(__GNUG__) || defined(__clang__)
    return 63 - __builtin_clzll(n);
#else
    int i = 0;
    while ((n >> (i + 1)) != 0) ++i;
    return i;
#endif
}

cpp_int a_n(uint64_t n) {
    if (n == 0) throw std::invalid_argument("n must be >= 1");
    if (n == 1) return 1;

    // (p,q) = (a(k), a(k+1)), starting at k=1: (1,2)
    cpp_int p = 1;
    cpp_int q = 2;

    int msb = msb_index(n);
    for (int bit = msb - 1; bit >= 0; --bit) {   // skip leading 1
        uint64_t b = (n >> bit) & 1ULL;

        if (b == 0) {
            // (p,q) <- (2p, p - 3q)
            cpp_int new_p = p << 1;      // 2*p
            cpp_int new_q = p - 3 * q;
            p = new_p;
            q = new_q;
        } else {
            // (p,q) <- (p - 3q, 2q)
            cpp_int new_p = p - 3 * q;
            cpp_int new_q = q << 1;      // 2*q
            p = new_p;
            q = new_q;
        }
    }
    return p; // a(n)
}

int main() {
    uint64_t n = 1000000000000ULL;
    cpp_int sum = 0;
    for (int i = 1; i <= n; ++i) {
        sum += a_n(i);
    }

    std::cout<<sum<<std::endl;
    // cpp_int ans = a_n(n);
    // std::cout << "a(" << n << ") = " << ans << "\n";
}