#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <vector>

using u64 = std::uint64_t;

u64 solve(u64 n = 1000000ULL) {
    u64 x = 1;
    std::vector<u64> values;
    while (true) {
        const u64 a = x * (x + 1);
        if (a > n / a) {
            break;
        }

        const u64 limit = n / a;
        u64 y = x;

        while (y <= limit / (y + 1)) {
            const u64 value = x * y * (x + 1) * (y + 1);
            if (value > n) {
                break;
            }

            values.push_back(value);
            ++y;
        }

        ++x;
    }

    std::sort(values.begin(), values.end());
    const u64 ans = std::unique(values.begin(), values.end()) - values.begin();
    return ans;
}

int main() {
    const auto start = std::chrono::steady_clock::now();
    std::cout << solve(100000000000000ULL) << '\n';
    const auto end = std::chrono::steady_clock::now();

    const std::chrono::duration<double> elapsed = end - start;
    std::cout << "Time taken: " << elapsed.count() << " seconds\n";
    return 0;
}
