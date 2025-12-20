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

static void solve_alternate();
static 
void  solve() {
    // Entry point: run the search and print the answer.
    
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
}


static 
void  solve_alternate() {
    // Entry point: run the search and print the answer.
    
    int64_t j = 1;
    int64_t p = 1;
    int64_t q = 2;
    int64_t sum_prev = 0;
    int64_t sum = 1;
    int64_t p_prev = 1;
    int64_t q_prev = 2;
    int64_t prev_half = 0;
    uint64_t limit = 1000000000000;
    string bin = toBinary(5*1e11);
    cout<<bin<<endl;

    // The sequence (p, q) tracks two consecutive terms a(k), a(k+1).
    // Walking the bits of n (after the leading 1) performs a
    // binary exponentiation-style recurrence:
    //   bit 0: (p, q) -> (2p, p - 3q)   corresponds to doubling k
    //   bit 1: (p, q) -> (p - 3q, 2q)   corresponds to doubling k and adding 1
    // After processing all bits, p holds a(n) and q holds a(n+1).
    for (char c = bin[j];c != '\0';c = bin[++j]) {
      if (c == '0') {
        q = p - 3 * q;
        p = 2 * p;
      }
      else {
        p = p - 3 * q;
        q = 2 * q;
      }
    }

    cout<<4-p<<" "<<q<<endl;
}



int main() {
  auto start = std::chrono::steady_clock::now();
  solve_alternate();
  auto end = std::chrono::steady_clock::now();
  std::chrono::duration<double> elapsed = end - start;
  std::cout << "Elapsed: " << elapsed.count() << " s\n";
}
