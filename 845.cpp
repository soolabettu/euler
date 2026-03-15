/* Project Euler Problem 845: https://projecteuler.net/problem=845 */
// Uses digit DP plus binary search to locate the target number whose digit sum is prime.

#include <iostream>
#include <vector>
#include <string>
#include <numeric>
#include <algorithm>
#include <sstream>
#include <cstring>

using namespace std;

static 
long long solve(int pos, int sum, int ub, int leading_zeroes, string& upper_limit, int& depth);

static
long long digit_sum(long long n);

static
void binary_search();

long long dp[40][200][2][2];
long long v[40][200][2][2];
// string upper_limit = "10000000000000000";


bool isPrime(long long n);
string s;

// Simple trial-division primality check used both by the digit DP and the
// post-processing loop. This is fine because the arguments are small (sum of
// digits) or infrequent (checking candidates near the binary search result).
bool isPrime(long long n) {
    if (n < 2) return false;
    for (long long i = 2; i * i <= n; i++) {
        if (n % i == 0) return false;
    }
    return true;
}

// dp[pos][sum%mod][ub][leading_zeroes]
// visited[pos][sum%mod][ub][leading_zeroes]

// Digit-DP recursion that counts how many numbers within the current prefix
// constraints produce a prime digit sum.
// pos            : index of the digit we are deciding (0 == most significant).
// sum            : accumulated digit sum so far.
// tight          : whether the prefix is still equal to the upper bound.
// leading_zeroes : true while we have only seen leading zeros (so sum=0
//                  does not falsely register as prime).
// upper_limit    : decimal string boundary for the search.
// depth          : number of digits under consideration.
static long long solve(int pos, int sum, int tight, int leading_zeroes,
                       string& upper_limit, int& depth) {

    if (pos == depth) {
        if (isPrime(sum)) {
            // cout<<pos<<" "<<sum<<" "<<isPrime(sum)<<endl;
        }
        
        return isPrime(sum) && leading_zeroes == 0;
    }

    if (v[pos][sum][tight][leading_zeroes]) {
        return dp[pos][sum][tight][leading_zeroes];
    }

    long long cnt =  0;
    int limit = tight ? upper_limit[pos] - '0' : 9;
    for (int i = 0; i <= limit; i++) {
        cnt += solve(pos + 1, (sum + i), tight && (i == limit), leading_zeroes && (i == 0), upper_limit, depth);
    }

    v[pos][sum][tight][leading_zeroes] = 1;
    return dp[pos][sum][tight][leading_zeroes] = cnt;
}


// Binary search for the smallest number whose count of prime-digit-sum numbers
// (up to that number) equals the Project Euler target, then walk backwards to
// find the exact value whose digit sum is itself prime.
static void binary_search() {
    long long low = 0;
    string upper_limit = "100000000000000000";
    long long high = stoll(upper_limit);
    long long mid = high;
    long long target = 10000000000000000;
    
    int depth = upper_limit.size();
    while (low < high) {
        mid = low + (high - low) / 2;
        s = to_string(mid);
        memset(v, 0, sizeof(v));
        memset(dp, 0, sizeof(dp));
        int depth = s.size();
        long long x = solve(0, 0, 1, 1, s, depth);
        if (x == target) {
            break;
        }

        if (x > target) {
            high = mid;
        } else {
            low = mid + 1;
        }
    }

    while(1) {
        if (isPrime(digit_sum(mid))) {
            cout<<mid<<endl;
            break;
        }

        mid -= 1;
    }
}

// Utility that returns the sum of decimal digits for n. Used to check whether
// a candidate found by binary_search has a prime digit sum.
long long digit_sum(long long n) {
    long long sum = 0;
    while (n != 0) {
        sum += n % 10;
        n /= 10;
    }
    return sum;
}


// Entry point: run the search and print the answer.
int main() {
    binary_search();
    return 0;
}
