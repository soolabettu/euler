#include <iostream>
#include <map>
#include <vector>
#include <chrono>

using namespace std;

vector<int> primes_list = { 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97 };

map<int, int> visited;

static void solve(int idx, long long total) {

    if (total > 1000000000|| visited[total]) {
        return;
    }

    visited[total] = 1;
    for (int i = idx; i < primes_list.size(); i++) {
        solve(i, total * primes_list[i]);
    }
}

int main()
{
   using clock = std::chrono::steady_clock;
   auto start = clock::now();
    solve(0, 1);
    auto stop = clock::now();
    cout<<visited.size()<<endl;
    double ms = std::chrono::duration<double, std::milli>(stop - start).count();
    std::cout << "Elapsed: " << ms/1000 << " seconds\n";
    return 0;
}
