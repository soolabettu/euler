/*
 * Project Euler 348: palindromic sums of a square and a cube.
 *
 * This is the C++ counterpart of 348.py.  It examines the same 98,990,100
 * square-cube pairs and reports the same five palindromes that have exactly
 * four representations.  Palindrome candidates live in an open-addressed
 * hash table, which provides the set membership and Counter behavior used by
 * the Python program without requiring a third-party library.
 */

#include <algorithm>
#include <chrono>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr std::uint64_t square_first = 10;
constexpr std::uint64_t square_limit = 100'000;
constexpr std::uint64_t cube_first = 10;
constexpr std::uint64_t cube_limit = 1'000;
constexpr std::size_t initial_table_capacity = 1'024;

struct PalindromeEntry {
    std::uint64_t key = 0;
    std::uint32_t count = 0;
};

class PalindromeTable {
public:
    PalindromeTable() : entries_(initial_table_capacity) {}

    void insert_candidate(std::uint64_t key)
    {
        if ((candidate_count_ + 1) * 10 >= entries_.size() * 7) {
            grow();
        }

        std::size_t slot = table_slot(key, entries_.size());
        while (entries_[slot].key != 0) {
            if (entries_[slot].key == key) {
                return;
            }
            slot = (slot + 1) & (entries_.size() - 1);
        }
        entries_[slot].key = key;
        ++candidate_count_;
    }

    void count_if_candidate(std::uint64_t key)
    {
        std::size_t slot = table_slot(key, entries_.size());

        while (entries_[slot].key != 0) {
            if (entries_[slot].key == key) {
                if (entries_[slot].count == 0) {
                    ++matched_count_;
                }
                ++entries_[slot].count;
                return;
            }
            slot = (slot + 1) & (entries_.size() - 1);
        }
    }

    [[nodiscard]] std::size_t matched_count() const
    {
        return matched_count_;
    }

    [[nodiscard]] const std::vector<PalindromeEntry>& entries() const
    {
        return entries_;
    }

private:
    static std::uint64_t hash_u64(std::uint64_t value)
    {
        value ^= value >> 30;
        value *= UINT64_C(0xbf58476d1ce4e5b9);
        value ^= value >> 27;
        value *= UINT64_C(0x94d049bb133111eb);
        value ^= value >> 31;
        return value;
    }

    static std::size_t table_slot(std::uint64_t key, std::size_t capacity)
    {
        return static_cast<std::size_t>(
            hash_u64(key) & static_cast<std::uint64_t>(capacity - 1));
    }

    static void place_existing(std::vector<PalindromeEntry>& entries,
                               PalindromeEntry value)
    {
        std::size_t slot = table_slot(value.key, entries.size());

        while (entries[slot].key != 0) {
            slot = (slot + 1) & (entries.size() - 1);
        }
        entries[slot] = value;
    }

    void grow()
    {
        if (entries_.size() > std::numeric_limits<std::size_t>::max() / 2) {
            throw std::length_error("palindrome table is too large");
        }

        std::vector<PalindromeEntry> replacement(entries_.size() * 2);
        for (const PalindromeEntry entry : entries_) {
            if (entry.key != 0) {
                place_existing(replacement, entry);
            }
        }
        entries_.swap(replacement);
    }

    std::vector<PalindromeEntry> entries_;
    std::size_t candidate_count_ = 0;
    std::size_t matched_count_ = 0;
};

std::uint64_t make_palindrome(std::uint64_t prefix, bool odd_length)
{
    std::uint64_t palindrome = prefix;
    std::uint64_t remainder = odd_length ? prefix / 10 : prefix;

    while (remainder != 0) {
        palindrome = palindrome * 10 + remainder % 10;
        remainder /= 10;
    }
    return palindrome;
}

void build_palindromes(PalindromeTable& table, std::uint64_t minimum,
                       std::uint64_t maximum)
{
    for (std::uint64_t prefix = 1;; ++prefix) {
        const std::uint64_t odd = make_palindrome(prefix, true);
        const std::uint64_t even = make_palindrome(prefix, false);

        if (odd > maximum && even > maximum) {
            break;
        }
        if (odd >= minimum && odd <= maximum) {
            table.insert_candidate(odd);
        }
        if (even >= minimum && even <= maximum) {
            table.insert_candidate(even);
        }
    }
}

std::string format_commas(std::uint64_t value)
{
    std::string digits = std::to_string(value);

    for (std::ptrdiff_t position = static_cast<std::ptrdiff_t>(digits.size()) - 3;
         position > 0; position -= 3) {
        digits.insert(static_cast<std::size_t>(position), 1, ',');
    }
    return digits;
}

} // namespace

int main()
{
    const auto start = std::chrono::steady_clock::now();
    std::vector<std::uint64_t> squares;
    std::vector<std::uint64_t> cubes;

    squares.reserve(static_cast<std::size_t>(square_limit - square_first));
    cubes.reserve(static_cast<std::size_t>(cube_limit - cube_first));

    for (std::uint64_t number = square_first; number < square_limit; ++number) {
        squares.push_back(number * number);
    }
    for (std::uint64_t number = cube_first; number < cube_limit; ++number) {
        cubes.push_back(number * number * number);
    }

    PalindromeTable table;
    build_palindromes(table, squares.front() + cubes.front(),
                      squares.back() + cubes.back());

    for (const std::uint64_t square : squares) {
        for (const std::uint64_t cube : cubes) {
            table.count_if_candidate(square + cube);
        }
    }

    std::vector<std::uint64_t> matching_sums;
    matching_sums.reserve(table.matched_count());
    for (const PalindromeEntry entry : table.entries()) {
        if (entry.key != 0 && entry.count == 4) {
            matching_sums.push_back(entry.key);
        }
    }
    std::sort(matching_sums.begin(), matching_sums.end());

    std::uint64_t matching_sum_total = 0;
    for (const std::uint64_t value : matching_sums) {
        matching_sum_total += value;
    }

    const auto finish = std::chrono::steady_clock::now();
    const std::chrono::duration<double> elapsed = finish - start;

    std::cout << "Stored " << format_commas(squares.size())
              << " squares in the squares set.\n"
              << "Smallest square: " << format_commas(squares.front()) << '\n'
              << "Largest square:  " << format_commas(squares.back()) << "\n\n"
              << "Stored " << format_commas(cubes.size())
              << " cubes in the cubes set.\n"
              << "Smallest cube: " << format_commas(cubes.front()) << '\n'
              << "Largest cube:  " << format_commas(cubes.back()) << "\n\n"
              << "Checked " << format_commas(squares.size() * cubes.size())
              << " square-cube pairings.\n"
              << "Found " << format_commas(table.matched_count())
              << " distinct palindromic sums.\n"
              << "Each entry has the form (palindromic_sum, occurrence_count).\n\n"
              << "Palindromic sums formed exactly four times: "
              << format_commas(matching_sums.size()) << '\n'
              << "Matching sums: [";

    for (std::size_t index = 0; index < matching_sums.size(); ++index) {
        std::cout << (index == 0 ? "" : ", ") << matching_sums[index];
    }

    std::cout << "]\n"
              << "Sum of matching palindromes: "
              << format_commas(matching_sum_total) << '\n'
              << "Elapsed time: " << std::fixed << std::setprecision(3)
              << elapsed.count() << " seconds\n";
    return EXIT_SUCCESS;
}
