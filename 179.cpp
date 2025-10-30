#include <iostream>
#include <map>
#include <chrono>
#include <cmath>

using namespace std;

void solve();

long limit = 1e7;
vector<long> nums(limit + 1, 2);

void solve() {
    for (long  i = 2; i < limit; i++) {
        for (long j = i; i * j < limit; j++) {
            if (i == j) {
                nums[i * j]++;   
            }
            else {
                nums[i * j] += 2;
            }
        }
    }

    int ans = 0;
    for (int i = 2; i < limit; i++) {
        if (nums[i] == nums[i + 1]) {
            ans++;
        }

        // cout<<i<<" "<<nums[i]<<" "<<i+1<<" "<<nums[i+1]<<endl;
    }   

    cout << ans << endl;
}

int main() {
    auto start = std::chrono::steady_clock::now();
    solve();
    auto end = std::chrono::steady_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::cout << "Elapsed: " << elapsed.count() << " s\n";
}
