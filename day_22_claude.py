from typing import List, Tuple, Dict
from itertools import product
from functools import lru_cache


def read_data(filename: str = "22.txt") -> List[int]:
    """Read initial secret numbers from file."""
    with open(filename) as f:
        return [int(line.strip()) for line in f]


@lru_cache(maxsize=None)
def next_secret(secret: int) -> int:
    """Generate the next secret number in the sequence using the specified rules."""
    # Rule 1: multiply by 64 and mix
    secret ^= secret * 64
    secret %= 16777216  # prune

    # Rule 2: divide by 32 (floor division) and mix
    secret ^= secret // 32
    secret %= 16777216  # prune

    # Rule 3: multiply by 2048 and mix
    secret ^= secret * 2048
    secret %= 16777216  # prune

    return secret


def get_price_sequence(initial: int, n: int = 2000) -> Tuple[List[int], List[int]]:
    """Generate sequence of prices and their changes."""
    prices = []
    secret = initial

    # Pre-generate all secrets and prices
    for _ in range(n + 1):  # +1 for initial price
        prices.append(secret % 10)
        secret = next_secret(secret)

    # Calculate changes
    changes = [prices[i + 1] - prices[i] for i in range(n)]

    return prices[1:], changes  # Remove first price as it has no change


def find_best_pattern(
    sequences_dict: Dict[int, Tuple[List[int], List[int]]],
) -> Tuple[Tuple[int, ...], int]:
    """Find pattern that yields maximum bananas using pre-computed sequences."""
    max_bananas = 0
    best_pattern = None

    # Consider only changes that actually occur in the sequences
    # Create a set of all possible changes
    possible_changes = set()
    for prices, changes in sequences_dict.values():
        possible_changes.update(changes[:4])  # Only need first 4 changes for patterns

    # Convert to list for product
    possible_changes = list(possible_changes)

    for pattern in product(possible_changes, repeat=4):
        total_bananas = 0
        for prices, changes in sequences_dict.values():
            # Use string matching for faster pattern search
            pattern_str = ",".join(map(str, pattern))
            changes_str = ",".join(map(str, changes))

            if pattern_str in changes_str:
                # Find the index where pattern occurs
                changes_list = changes_str.split(",")
                for i in range(len(changes_list) - 3):
                    if tuple(map(int, changes_list[i : i + 4])) == pattern:
                        total_bananas += prices[i + 3]
                        break

        if total_bananas > max_bananas:
            max_bananas = total_bananas
            best_pattern = pattern

    return best_pattern, max_bananas


def part1(initial_secrets: List[int], n: int = 2000) -> int:
    """Calculate the sum of the nth secret number for each initial secret."""
    return sum(generate_nth_secret(initial, n) for initial in initial_secrets)


def part2(initial_secrets: List[int], n: int = 2000) -> int:
    """Find the maximum number of bananas possible."""
    # Pre-compute all sequences
    sequences_dict = {
        initial: get_price_sequence(initial, n) for initial in initial_secrets
    }

    best_pattern, max_bananas = find_best_pattern(sequences_dict)
    print(f"Best pattern of changes: {best_pattern}")
    return max_bananas


def generate_nth_secret(initial: int, n: int) -> int:
    """Generate the nth secret number in the sequence."""
    secret = initial
    for _ in range(n):
        secret = next_secret(secret)
    return secret


def main():
    initial_secrets = read_data()

    result1 = part1(initial_secrets)
    print(f"Part 1 - Sum of 2000th secret numbers: {result1}")

    result2 = part2(initial_secrets)
    print(f"Part 2 - Maximum bananas possible: {result2}")


if __name__ == "__main__":
    main()
