#include <iostream>
#include <map>
#include <vector>
#include <chrono>
#include <iomanip>

using namespace std;

// dp[state] caches the expected number of future draws given an exact state so
// we do not recompute overlapping subproblems in the recursion tree.
map<vector<int>, double> dp;

static double solve(vector<int>& state) {
    // `state` encodes the entire game configuration:
    //   state[0..4] : how many tokens currently sit in each bucket of distance i
    //   state[5]    : the length of the chain that was just processed (used to
    //                 avoid counting the same bucket twice in a row).
    // The function returns the expected number of further turns starting from
    // this configuration.

    // If we have evaluated this configuration before, reuse the cached result.
    if (dp[state]) {
        return dp[state];
    }

    // K is the total "weight" that determines the probability of picking each
    // bucket: a bucket at distance i is i times as likely to be chosen as the
    // base bucket.
    int K = 0;
    for (int i = 0;i < 5;++i) {
        K += i * state[i];
    }
    
    if (K == 0) {
        // No weighted tokens left, so there are no future turns.
        return 0;
    }

    // Expected value contributed by all possible moves.
    double ev = 0;
    for (int i = 1;i < 5;++i) {
        if (state[i] == 0) {
            continue;
        }

        // Simulate choosing a bucket at distance i and moving a token one step
        // closer to the start.
        vector<int> new_state = state;
        new_state[i] -= 1;
        new_state[i - 1] += 1;
        new_state[5] = i - 1;

        // Probability of selecting this bucket is proportional to: distance i
        // times the number of available tokens, minus one if the previously
        // moved bucket matches (state[5] == i), because that token is already
        // accounted for.
        ev += solve(new_state) * (i * (state[i] - (state[5] == i))) / K;
    }
    
    // Store and return the total expected turns (1 for the current move plus
    // the weighted future expectation).
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
