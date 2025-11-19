#include<bits/stdc++.h>

using namespace std;

map<vector<int>, double> dp;

static double solve(vector<int>& state) {
    if (dp[state]) {
        return dp[state];
    }

    int K = 0;
    for (int i = 0;i < 5;++i) {
        K += i * state[i];
    }
    
    if (K == 0) {
        return 0;
    }

    double ev = 0;
    for (int i = 1;i < 5;++i) {
        if (state[i] == 0) {
            continue;
        }
        vector<int> new_state = state;
        new_state[i] -= 1;
        new_state[i - 1] += 1;
        new_state[5] = i - 1;
        ev += solve(new_state) * (i * (state[i] - (state[5] == i))) / K;
    }
    
    return dp[state] = 1 + ev;
}

int main() {

    using clock = std::chrono::steady_clock;
    auto start = clock::now();
    vector<int> state = {0, 0, 0, 1, 12, 3};
    cout<<setprecision(10)<<1 + solve(state)<<endl;
    auto stop = clock::now();
    double ms = std::chrono::duration<double, std::milli>(stop - start).count();
    std::cout << "Elapsed: " << ms/1000 << " seconds\n";
    return 0;
}

