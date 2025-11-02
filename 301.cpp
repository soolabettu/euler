#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <unordered_map>
#include <utility>
#include <vector>

// Direct translation of helper routines from 301.py -------------------------


std::uint64_t solve(std::uint64_t limit = 1ULL << 30) {
    std::uint64_t cnt = 0;
    for (std::uint64_t n = 1; n <= limit; ++n) {
        std::uint64_t x = n;
        std::uint64_t y = n * 2;
        std::uint64_t z = n * 3;
        if (((x ^ y) ^ z) == 0) {
            ++cnt;
        }
    }
    return cnt;
}

int main() {
    auto start = std::chrono::steady_clock::now();
    std::uint64_t result = solve();
    auto end = std::chrono::steady_clock::now();

    std::chrono::duration<double> elapsed = end - start;
    std::cout << result << '\n';
    std::cout << "Elapsed: " << elapsed.count() << " s\n";
    return 0;
}
