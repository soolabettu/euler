#include <iostream>
#include <chrono>

using namespace std;


std::string toBinary(int64_t n) {
    if (n == 0) {
        return "0";
    }
    std::string bits;
    while (n > 0) {
        bits.push_back((n & 1ULL) ? '1' : '0');
        n >>= 1;
    }
    std::reverse(bits.begin(), bits.end());
    return bits;
}

static void solve();
int main() {
    // Entry point: run the search and print the answer.
    auto start = std::chrono::steady_clock::now();
    int64_t j = 1;
    int64_t p = 1;
    int64_t q = 2;
    int64_t sum_prev = 0;
    int64_t sum = 1;
    int64_t p_prev = 1;
    int64_t q_prev = 2;
    int64_t prev_half = 0;
    uint64_t limit = 1000000000000;
    string bin = toBinary(limit);
    cout<<bin<<endl;
    for (char c = bin[j];c != '\0';c = bin[++j]) {
      if (c == '0') {
        q = p - 3 * q;
        p = 2 * p;
        sum = 4 + sum_prev - sum;
        sum_prev = sum - p;
      }
      else {
        sum_prev = 4 + sum_prev - sum;
        p = p - 3 * q;
        q = 2 * q;
        sum = sum_prev + p;
      }
    }

    cout<<sum_prev<<" "<<sum<<endl;

    auto end = std::chrono::steady_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::cout << "Elapsed: " << elapsed.count() << " s\n";
    return 0;
}
