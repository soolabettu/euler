#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <set>
#include <string>
#include <vector>

using namespace std;

static vector<int> generate_primes(int n) {
    if (n < 2) {
        return {};
    }

    vector<bool> sieve(n + 1, true);
    sieve[0] = false;
    sieve[1] = false;

    int limit = static_cast<int>(sqrt(n));
    for (int p = 2; p <= limit; ++p) {
        if (sieve[p]) {
            for (int multiple = p * p; multiple <= n; multiple += p) {
                sieve[multiple] = false;
            }
        }
    }

    vector<int> primes;
    for (int num = 2; num <= n; ++num) {
        if (sieve[num]) {
            primes.push_back(num);
        }
    }
    return primes;
}

static bool is_prime(int64_t n) {
    if (n < 2) {
        return false;
    }
    if (n == 2) {
        return true;
    }
    if (n % 2 == 0) {
        return false;
    }

    int64_t limit = static_cast<int64_t>(sqrt(static_cast<long double>(n)));
    for (int64_t factor = 3; factor <= limit; factor += 2) {
        if (n % factor == 0) {
            return false;
        }
    }
    return true;
}

static int64_t reverse_number(int64_t n) {
    string digits = to_string(n);
    reverse(digits.begin(), digits.end());
    return stoll(digits);
}

static void solve() {
    vector<int> primes = generate_primes(100000000);
    set<int64_t> ans;

    for (int p : primes) {
        int64_t r = reverse_number(p);
        int64_t s = 1LL * p * p;
        if (reverse_number(s) == s) {
            continue;
        }

        if (is_prime(r)) {
            int64_t t = r * r;
            string reversed_t = to_string(t);
            reverse(reversed_t.begin(), reversed_t.end());
            if (to_string(s) == reversed_t) {
                ans.insert(s);
                ans.insert(t);
                if (ans.size() == 50) {
                    break;
                }
            }
        }
    }

    int64_t total = accumulate(ans.begin(), ans.end(), 0LL);
    cout << ans.size() << ' ' << total << '\n';
}

int main() {
    auto start = chrono::steady_clock::now();
    solve();
    auto end = chrono::steady_clock::now();
    chrono::duration<double> elapsed = end - start;
    cout << "Elapsed: " << elapsed.count() << " s\n";
}
