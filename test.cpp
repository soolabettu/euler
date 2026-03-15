// Recursively enumerates factor combinations to recover minimal product-sum numbers for testing.

#include <iostream>


constexpr uint64_t M = 12000;
uint64_t m[M + 1];
void f(uint64_t product, uint64_t sum, uint64_t sum_size, uint64_t biggest_factor)
{
    auto n = product - sum + sum_size;
    if (n <= M && (m[n] == 0 || m[n] > product))
        m[n] = product;
    for (int i = biggest_factor; product * i <= 2 * M; i++)
        f(product * i, sum + i, sum_size + 1, i);
}

int main()
{
    for (auto &n : m)
        n = 0;
    f(1, 0, 0, 2);
    set<uint64_t> sln;
    for (auto n : m)
        sln.insert(n);
    uint64_t total = 0;
    for (auto n : sln)
        total += n;
    total -= 1;
    cout << total;
 }
