/* Project Euler Problem 323: https://projecteuler.net/problem=323 */
// Simulates random 32-bit masks and measures how many OR operations are needed to set every bit.

#include <chrono>
#include <cstdint>
#include <iostream>
#include <random>

// Random number generator shared across calls.
static std::mt19937_64 rng{std::random_device{}()};
static constexpr uint64_t LIMIT_32 = (1ULL << 32) - 1;

// Mirrors the Python solve(): keep OR-ing random 32-bit values until all bits are set.
static uint64_t solve() {
    uint64_t xprev = 0;
    std::uniform_int_distribution<uint64_t> dist(0, LIMIT_32);
    uint64_t yprev = dist(rng);

    uint64_t iterations = 0;
    while (true) {
        ++iterations;
        uint64_t xnext = xprev | yprev;
        if (xnext == LIMIT_32) {
            break;
        }
        xprev = xnext;
        yprev = dist(rng);
    }
    return iterations;
}

int main() {
    auto start = std::chrono::steady_clock::now();

    const uint64_t limit = 1'000'000'000ULL;
    unsigned long long total = 0;
    for (uint64_t i = 0; i < limit; ++i) {
        total += solve();
    }

    double average = static_cast<double>(total) / static_cast<double>(limit);
    std::cout << average << '\n';

    auto end = std::chrono::steady_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::cout << "Elapsed: " << elapsed.count() << " s\n";
    return 0;
}
