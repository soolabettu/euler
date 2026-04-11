#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <vector>

using u64 = std::uint64_t;

u64 solve(u64 n = 1'000'000ULL) {
    std::vector<u64> values;
    for (u64 x = 1;; ++x) {
        const u64 a = x * (x + 1);
        if (a > n / a) {
            break;
        }

        const u64 limit = n / a;
        for (u64 y = x; y <= limit / (y + 1); ++y) {
            values.push_back(a * y * (y + 1));
        }
    }

    std::sort(values.begin(), values.end());
    values.erase(std::unique(values.begin(), values.end()), values.end());
    return values.size();
}

int main() {
    const auto start = std::chrono::steady_clock::now();
    std::cout << solve(100000000000000ULL) << '\n';
    const auto end = std::chrono::steady_clock::now();

    const std::chrono::duration<double> elapsed = end - start;
    std::cout << "Time taken: " << elapsed.count() << " seconds\n";
    return 0;
}
