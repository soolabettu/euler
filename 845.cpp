#include <iostream>
#include <vector>
#include <string>
#include <numeric>
#include <algorithm>

using namespace std;

static 
long long solve(int pos, int sum, int ub, int leading_zeroes, string& upper_limit);

long long dp[40][200][2][2];
long long v[40][200][2][2];
string upper_limit = "10000000000000000";
int depth = upper_limit.size();

bool isPrime(long long n);

bool isPrime(long long n) {
    if (n < 2) return false;
    for (long long i = 2; i * i <= n; i++) {
        if (n % i == 0) return false;
    }
    return true;
}

// dp[pos][sum%mod][ub][leading_zeroes]
// visited[pos][sum%mod][ub][leading_zeroes]

static
long long solve(int pos, int sum, int tight, int leading_zeroes, string& upper_limit) {

    if (pos == depth) {
        if (isPrime(sum)) {
            cout<<pos<<" "<<sum<<" "<<isPrime(sum)<<endl;
        }
        
        return isPrime(sum) && leading_zeroes == 0;
    }

    if (v[pos][sum][tight][leading_zeroes]) {
        return dp[pos][sum][tight][leading_zeroes];
    }

    long long cnt =  0;
    int limit = tight ? upper_limit[pos] - '0' : 9;
    for (int i = 0; i <= limit; i++) {
        cnt += solve(pos + 1, (sum + i), tight && (i == limit), leading_zeroes && (i == 0), upper_limit);
    }

    v[pos][sum][tight][leading_zeroes] = 1;
    return dp[pos][sum][tight][leading_zeroes] = cnt;
}


int main() {
    cout<<solve(0, 0, 1, 1, upper_limit)<<endl;
    return 0;
}
