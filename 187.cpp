#include <iostream>
#include <map>
#include <chrono>
#include <cmath>
#include <vector>
#include <algorithm>

using namespace std;

void solve();
bool isPrime(long long n);
std::vector<long long> primesUpTo(long long n);

bool isPrime(long long n) {
    if (n < 2) return false;
    if (n % 2 == 0) return n == 2;
    if (n % 3 == 0) return n == 3;

    long long limit = static_cast<long long>(sqrt(static_cast<long double>(n)));
    for (long long i = 5; i <= limit; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) return false;
    }
    return true;
}

std::vector<long long> primesUpTo(long long n) {
    if (n < 2) return {};

    std::vector<bool> is_prime(static_cast<std::size_t>(n) + 1, true);
    is_prime[0] = false;
    is_prime[1] = false;

    long long root = static_cast<long long>(sqrt(static_cast<long double>(n)));
    for (long long i = 2; i <= root; ++i) {
        if (!is_prime[static_cast<std::size_t>(i)]) continue;
        for (long long j = i * i; j <= n; j += i) {
            is_prime[static_cast<std::size_t>(j)] = false;
        }
    }

    std::vector<long long> primes;
    auto log_input = n > 3 ? static_cast<long double>(n) : static_cast<long double>(3);
    auto estimate = log_input > 0.0L ? static_cast<std::size_t>(n / std::log(log_input)) : static_cast<std::size_t>(0);
    primes.reserve(std::max<std::size_t>(estimate, 1));
    for (long long i = 2; i <= n; ++i) {
        if (is_prime[static_cast<std::size_t>(i)]) {
            primes.push_back(i);
        }
    }
    return primes;
}

void solve() {
    long limit = 1e8;
    auto primes = primesUpTo(limit);
    long sz = primes.size();
    vector<long> dp(limit, 0);
    for (long i = 0; i < sz; i++) {
        for (long j = 0; j < sz && primes[i] * primes[j] < limit; j++) {
            dp[primes[i] * primes[j]] = 1;
        }
    }

    int cnt = 0;
    for (int i = 0;i < limit;i++) {
        if (dp[i] == 1) {
            cnt += 1;
        }
    }

    cout<<cnt<<endl;
}

int main() {
    auto start = std::chrono::steady_clock::now();
    solve();
    auto end = std::chrono::steady_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::cout << "Elapsed: " << elapsed.count() << " s\n";
}
