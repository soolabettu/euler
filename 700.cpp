#include <iostream>
#include <map>
#include <vector>
#include <chrono>
#include <set>
#include <numeric>
#include <unistd.h>



using namespace std;

static tuple< int64_t,  int64_t> eec(int64_t a,  int64_t b,  int64_t c,  int64_t d);

static void binary_search();

/**
 * Naively scanning the Eulercoin sequence by adding the seed would take millions
 * of iterations before each new record is found. This routine instead performs
 * a literal binary search on the torus Z_mod: low/high delimit the arc that
 * still contains the next record value. At each step we take the modular
 * midpoint (low + high) mod mod. If the addition wraps around (mid < low) the
 * midpoint falls into the “lower” arc and is therefore a new record, so low is
 * updated. Otherwise the midpoint sits “above” the current record and shrinks
 * the upper bound. Because gcd(seed, mod) = 1, the additive sequence visits
 * every residue exactly once, so repeatedly halving the remaining arc is
 * guaranteed to encounter every Eulercoin (every new record low of the modular
 * sequence).
 *
 * Number-theoretically, these record lows are the “best lower approximations”
 * (convergents) of seed/mod, so the same structure appears in Farey sequences,
 * the Stern–Brocot tree, and continued fractions. Taking the modular midpoint
 * mirrors forming mediants in the Stern–Brocot tree: mediants that fall below
 * the irrational slope become the next convergent/Eulercoin, whereas the others
 * tighten the upper bound. This is also equivalent to the dual Beatty sequences
 * used in solve(), where the inverse sweep enumerates the complementary set of
 * convergents.
 */
static void binary_search() {
    uint64_t low = 1504170715041707LL;
    uint64_t high = low;
    uint64_t inc = 1504170715041707LL;
    uint64_t sum = 1504170715041707LL;
    uint64_t mod = 4503599627370517LL;
    uint64_t mid = 1504170715041707LL;
    while (low > 0)  {
        mid = (low + high) % mod;
        if (mid < low) {
            low = mid;
            sum += mid;
        }
        else  {
            high = mid;
        }

        cout<<low<<" "<<high<<endl;
    }

    cout<< sum << endl;
}

static tuple< int64_t,  int64_t> eec ( int64_t a,  int64_t b,  int64_t c,  int64_t d,  int64_t e,  int64_t f) {
    int64_t r = b % a;
    int64_t q = - b / a;
    if (r == 0) {
        return make_tuple(e, f);
    }
    else {
        tuple< int64_t,  int64_t> result = eec(r, a, e, f, c + q * e, d + q * f);
        return result;
    }
}

static void solve() {
    // Compute Bézout coefficients for (seed, modulus); used to derive the inverse.
    tuple< int64_t,  int64_t> result = eec(1504170715041707LL, 4503599627370517LL, 0LL, 1LL, 1LL, 0LL);
    // Core constants from Project Euler 700.
    uint64_t mod = 4503599627370517;
    uint64_t fterm = 1504170715041707;
    uint64_t inv;
    // Normalize the inverse into [0, mod) if the extended GCD returned a negative value.
    if (get<0>(result) < 0) {
        inv = get<0>(result) + mod;
    }

    // Track the forward scan (start_*) and reverse scan (end_*).
    uint64_t end = inv;
    uint64_t end_min = 4503599627370517 - 1;
    uint64_t end_idx = 1;
    uint64_t start_index = 1;
    vector<uint64_t> start_list;
    vector<uint64_t> end_list;
    // Seed both lists with the first Eulercoin value.
    start_list.push_back(fterm);
    end_list.push_back(1);
    uint64_t start = fterm;
    // Iterate until the forward and reverse sweeps have crossed.
    while (start_index < end_min) {
        // Advance the forward sequence and keep only new record lows.
        start = (start + fterm) % mod;
        if (start < start_list.back()) {
            start_list.push_back(start);
        }

        // Advance the inverse-based sequence and record new minima there as well.
        end_idx += 1;
        end = (inv + end) % mod;
        if (end < end_min) {
            end_min = end;
            end_list.push_back(end_idx);
        }

        start_index += 1;
    }

    // Combine the indices from both passes and sum the unique ones.
    set<uint64_t> v;
    v.insert(start_list.begin(), start_list.end());
    v.insert(end_list.begin(), end_list.end());
    uint64_t sum = accumulate(v.begin(), v.end(), 0LL);
    
    cout<<sum<<endl;
}




int main() {
    using clock = std::chrono::steady_clock;
    auto start = clock::now();
    // solve();
    binary_search();
    auto stop = clock::now();
    double ms = std::chrono::duration<double, std::milli>(stop - start).count();
    std::cout << "Elapsed: " << ms/1000 << " seconds\n";
    return 0;
}
