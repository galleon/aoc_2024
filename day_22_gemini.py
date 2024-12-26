def read_data(filename):
    with open(filename, "r") as f:
        return [int(line.strip()) for line in f]


def mix(secret, value):
    return secret ^ value


def prune(secret):
    return secret % 16777216


def generate_next_secret(secret):
    secret = mix(secret, prune(secret * 64))
    secret = mix(secret, prune(secret // 32))
    secret = mix(secret, prune(secret * 2048))
    return secret


def part1(initial_secrets):
    total_sum = 0
    for initial_secret in initial_secrets:
        secret = initial_secret
        for _ in range(2000):
            secret = generate_next_secret(secret)
        total_sum += secret
    return total_sum


def part1_optimized(initial_secrets):
    total_sum = 0
    for initial_secret in initial_secrets:
        secret = initial_secret
        # Precompute the sequence for each initial secret
        secrets = [secret]
        for _ in range(2000):
            secret = generate_next_secret(secret)
            secrets.append(secret)
        total_sum += secrets[2000]
    return total_sum


def part1_optimized_with_cache(initial_secrets):
    total_sum = 0
    cache = {}
    for initial_secret in initial_secrets:
        if initial_secret in cache:
            total_sum += cache[initial_secret]
            continue

        secret = initial_secret
        secrets = [secret]
        for _ in range(2000):
            secret = generate_next_secret(secret)
            secrets.append(secret)
        cache[initial_secret] = secrets[2000]
        total_sum += secrets[2000]
    return total_sum


def mix(secret, value):
    return secret ^ value


def prune(secret):
    return secret % 16777216


def generate_next_secret(secret):
    secret = mix(secret, prune(secret * 64))
    secret = mix(secret, prune(secret // 32))
    secret = mix(secret, prune(secret * 2048))
    return secret


def generate_prices(initial_secret, num_prices=2001):
    secrets = [initial_secret]
    for _ in range(num_prices - 1):
        secrets.append(generate_next_secret(secrets[-1]))
    return [secret % 10 for secret in secrets]


def calculate_changes(prices):
    return [prices[i] - prices[i - 1] for i in range(1, len(prices))]


def part2(initial_secrets):
    max_bananas = 0
    best_sequence = None

    price_sequences = [generate_prices(secret) for secret in initial_secrets]
    change_sequences = [calculate_changes(prices) for prices in price_sequences]

    possible_changes = set()
    for changes in change_sequences:
        possible_changes.update(changes)

    possible_sequences = []
    for c1 in possible_changes:
        for c2 in possible_changes:
            for c3 in possible_changes:
                for c4 in possible_changes:
                    possible_sequences.append((c1, c2, c3, c4))

    for sequence in possible_sequences:
        total_bananas = 0
        for i, changes in enumerate(change_sequences):
            for j in range(len(changes) - 3):
                if changes[j : j + 4] == list(sequence):
                    total_bananas += price_sequences[i][j + 4]
                    break  # Only sell once per buyer
        if total_bananas > max_bananas:
            max_bananas = total_bananas
            best_sequence = sequence

    return max_bananas


def main():
    initial_secrets = read_data("22.txt")
    result = part1_optimized_with_cache(initial_secrets)
    print(result)
    result = part2(initial_secrets)
    print(result)


if __name__ == "__main__":
    main()
