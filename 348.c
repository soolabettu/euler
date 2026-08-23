#define _POSIX_C_SOURCE 200809L

/*
 * Project Euler 348: palindromic sums of a square and a cube.
 *
 * This is the C counterpart of 348.py.  It examines the same 98,990,100
 * square-cube pairs and reports the same five palindromes that have exactly
 * four representations.  Palindrome candidates live in an open-addressed
 * hash table, which provides the set membership and Counter behavior used by
 * the Python program without requiring a third-party library.
 */

#include <inttypes.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

enum {
    SQUARE_FIRST = 10,
    SQUARE_LIMIT = 100000,
    CUBE_FIRST = 10,
    CUBE_LIMIT = 1000,
    INITIAL_TABLE_CAPACITY = 1024
};

typedef struct {
    uint64_t key;
    uint32_t count;
} PalindromeEntry;

typedef struct {
    PalindromeEntry *entries;
    size_t capacity;
    size_t candidate_count;
    size_t matched_count;
} PalindromeTable;

static void fail(const char *message)
{
    fprintf(stderr, "%s\n", message);
    exit(EXIT_FAILURE);
}

static void *checked_calloc(size_t count, size_t size)
{
    void *memory = calloc(count, size);

    if (memory == NULL) {
        fail("memory allocation failed");
    }
    return memory;
}

/* SplitMix64's finalizer gives sequential palindrome keys a well-spread hash. */
static uint64_t hash_u64(uint64_t value)
{
    value ^= value >> 30;
    value *= UINT64_C(0xbf58476d1ce4e5b9);
    value ^= value >> 27;
    value *= UINT64_C(0x94d049bb133111eb);
    value ^= value >> 31;
    return value;
}

static size_t table_slot(uint64_t key, size_t capacity)
{
    return (size_t)(hash_u64(key) & (uint64_t)(capacity - 1));
}

static void table_init(PalindromeTable *table)
{
    table->capacity = INITIAL_TABLE_CAPACITY;
    table->candidate_count = 0;
    table->matched_count = 0;
    table->entries = checked_calloc(table->capacity, sizeof(*table->entries));
}

static void table_place_existing(PalindromeEntry *entries, size_t capacity,
                                 PalindromeEntry value)
{
    size_t slot = table_slot(value.key, capacity);

    while (entries[slot].key != 0) {
        slot = (slot + 1) & (capacity - 1);
    }
    entries[slot] = value;
}

static void table_grow(PalindromeTable *table)
{
    const size_t old_capacity = table->capacity;
    PalindromeEntry *old_entries = table->entries;
    size_t index;

    if (old_capacity > SIZE_MAX / 2) {
        fail("palindrome table is too large");
    }
    table->capacity *= 2;
    table->entries = checked_calloc(table->capacity, sizeof(*table->entries));

    for (index = 0; index < old_capacity; ++index) {
        if (old_entries[index].key != 0) {
            table_place_existing(table->entries, table->capacity,
                                 old_entries[index]);
        }
    }
    free(old_entries);
}

static void table_insert_candidate(PalindromeTable *table, uint64_t key)
{
    size_t slot;

    /* Keep the linear-probing table below a 70 percent load factor. */
    if ((table->candidate_count + 1) * 10 >= table->capacity * 7) {
        table_grow(table);
    }

    slot = table_slot(key, table->capacity);
    while (table->entries[slot].key != 0) {
        if (table->entries[slot].key == key) {
            return;
        }
        slot = (slot + 1) & (table->capacity - 1);
    }
    table->entries[slot].key = key;
    table->entries[slot].count = 0;
    ++table->candidate_count;
}

static void table_count_if_candidate(PalindromeTable *table, uint64_t key)
{
    size_t slot = table_slot(key, table->capacity);

    while (table->entries[slot].key != 0) {
        if (table->entries[slot].key == key) {
            if (table->entries[slot].count == 0) {
                ++table->matched_count;
            }
            ++table->entries[slot].count;
            return;
        }
        slot = (slot + 1) & (table->capacity - 1);
    }
}

static uint64_t make_palindrome(uint64_t prefix, bool odd_length)
{
    uint64_t palindrome = prefix;
    uint64_t remainder = odd_length ? prefix / 10 : prefix;

    while (remainder != 0) {
        palindrome = palindrome * 10 + remainder % 10;
        remainder /= 10;
    }
    return palindrome;
}

static void build_palindromes(PalindromeTable *table, uint64_t minimum,
                              uint64_t maximum)
{
    uint64_t prefix = 1;

    for (;;) {
        const uint64_t odd = make_palindrome(prefix, true);
        const uint64_t even = make_palindrome(prefix, false);

        if (odd > maximum && even > maximum) {
            break;
        }
        if (odd >= minimum && odd <= maximum) {
            table_insert_candidate(table, odd);
        }
        if (even >= minimum && even <= maximum) {
            table_insert_candidate(table, even);
        }
        ++prefix;
    }
}

static int compare_u64(const void *left, const void *right)
{
    const uint64_t a = *(const uint64_t *)left;
    const uint64_t b = *(const uint64_t *)right;

    return (a > b) - (a < b);
}

static double elapsed_seconds(struct timespec start, struct timespec finish)
{
    return (double)(finish.tv_sec - start.tv_sec)
           + (double)(finish.tv_nsec - start.tv_nsec) / 1000000000.0;
}

static void format_commas(uint64_t value, char output[static 32])
{
    char reversed[32];
    size_t length = 0;
    size_t digit_count = 0;
    size_t output_index = 0;

    do {
        if (digit_count != 0 && digit_count % 3 == 0) {
            reversed[length++] = ',';
        }
        reversed[length++] = (char)('0' + value % 10);
        ++digit_count;
        value /= 10;
    } while (value != 0);

    while (length != 0) {
        output[output_index++] = reversed[--length];
    }
    output[output_index] = '\0';
}

int main(void)
{
    const size_t square_count = SQUARE_LIMIT - SQUARE_FIRST;
    const size_t cube_count = CUBE_LIMIT - CUBE_FIRST;
    uint64_t *squares;
    uint64_t *cubes;
    PalindromeTable table;
    uint64_t *matching_sums;
    size_t matching_count = 0;
    uint64_t matching_sum_total = 0;
    struct timespec start;
    struct timespec finish;
    size_t index;
    char formatted[32];

    if (clock_gettime(CLOCK_MONOTONIC, &start) != 0) {
        fail("could not read the monotonic clock");
    }

    squares = checked_calloc(square_count, sizeof(*squares));
    cubes = checked_calloc(cube_count, sizeof(*cubes));

    for (index = 0; index < square_count; ++index) {
        const uint64_t number = (uint64_t)(index + SQUARE_FIRST);
        squares[index] = number * number;
    }
    for (index = 0; index < cube_count; ++index) {
        const uint64_t number = (uint64_t)(index + CUBE_FIRST);
        cubes[index] = number * number * number;
    }

    table_init(&table);
    build_palindromes(&table, squares[0] + cubes[0],
                      squares[square_count - 1] + cubes[cube_count - 1]);

    for (size_t square_index = 0; square_index < square_count; ++square_index) {
        const uint64_t square = squares[square_index];

        for (size_t cube_index = 0; cube_index < cube_count; ++cube_index) {
            table_count_if_candidate(&table, square + cubes[cube_index]);
        }
    }

    matching_sums = checked_calloc(table.matched_count, sizeof(*matching_sums));
    for (index = 0; index < table.capacity; ++index) {
        if (table.entries[index].key != 0 && table.entries[index].count == 4) {
            matching_sums[matching_count++] = table.entries[index].key;
        }
    }
    qsort(matching_sums, matching_count, sizeof(*matching_sums), compare_u64);

    for (index = 0; index < matching_count; ++index) {
        matching_sum_total += matching_sums[index];
    }

    if (clock_gettime(CLOCK_MONOTONIC, &finish) != 0) {
        fail("could not read the monotonic clock");
    }

    format_commas((uint64_t)square_count, formatted);
    printf("Stored %s squares in the squares set.\n", formatted);
    format_commas(squares[0], formatted);
    printf("Smallest square: %s\n", formatted);
    format_commas(squares[square_count - 1], formatted);
    printf("Largest square:  %s\n", formatted);

    format_commas((uint64_t)cube_count, formatted);
    printf("\nStored %s cubes in the cubes set.\n", formatted);
    format_commas(cubes[0], formatted);
    printf("Smallest cube: %s\n", formatted);
    format_commas(cubes[cube_count - 1], formatted);
    printf("Largest cube:  %s\n", formatted);

    format_commas((uint64_t)square_count * (uint64_t)cube_count, formatted);
    printf("\nChecked %s square-cube pairings.\n", formatted);
    format_commas((uint64_t)table.matched_count, formatted);
    printf("Found %s distinct palindromic sums.\n", formatted);
    printf("Each entry has the form (palindromic_sum, occurrence_count).\n");

    format_commas((uint64_t)matching_count, formatted);
    printf("\nPalindromic sums formed exactly four times: %s\n", formatted);
    printf("Matching sums: [");
    for (index = 0; index < matching_count; ++index) {
        printf("%s%" PRIu64, index == 0 ? "" : ", ", matching_sums[index]);
    }
    printf("]\n");
    format_commas(matching_sum_total, formatted);
    printf("Sum of matching palindromes: %s\n", formatted);
    printf("Elapsed time: %.3f seconds\n", elapsed_seconds(start, finish));

    free(matching_sums);
    free(table.entries);
    free(cubes);
    free(squares);
    return EXIT_SUCCESS;
}
