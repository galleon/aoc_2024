def read_data():
    """
    Reads each line from '21.txt', returning a list of initial secret numbers (integers).
    """
    buyers = []
    with open("22.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                buyers.append(int(line))
    return buyers


def evolve(secret):
    """
    Performs one evolution step on secret (per puzzle instructions):
      1) secret = (secret XOR (secret*64))   & 0xFFFFFF
      2) secret = (secret XOR (secret//32)) & 0xFFFFFF
      3) secret = (secret XOR (secret*2048))& 0xFFFFFF
    Returns the new secret.
    """
    MOD_MASK = 0xFFFFFF

    # Step 1
    secret ^= secret << 6
    secret &= MOD_MASK

    # Step 2
    secret ^= secret >> 5
    secret &= MOD_MASK

    # Step 3
    secret ^= secret << 11
    secret &= MOD_MASK

    return secret


def generate_prices(initial_secret, length=2000):
    """
    Given an initial secret number, generate (length+1) secret numbers (including the initial),
    then convert them to prices (the ones digit).

    Returns a list of length (length+1) prices.
    """
    prices = []
    secret = initial_secret

    # Record initial price
    prices.append(secret % 10)

    # Generate 'length' new secrets and record their prices
    for _ in range(length):
        secret = evolve(secret)
        prices.append(secret % 10)

    return prices


def build_pattern_dict(prices):
    """
    Given a list of prices (length = 2001 if we generate 2000 new secrets),
    build a dictionary mapping (d0, d1, d2, d3) -> earliest price at which
    the monkey would sell.

    That is, if we see changes c[i],c[i+1],c[i+2],c[i+3] match a pattern,
    then we sell at prices[i+4] (the price following that last change).

    We store ONLY the earliest occurrence (smallest i) for each pattern.
    """
    pattern_dict = {}

    # We have len(prices) - 1 changes in total
    # Each pattern of 4 changes starts at i, i+1, i+2, i+3 => sells at i+4
    for i in range(len(prices) - 4):
        c0 = prices[i + 1] - prices[i]
        c1 = prices[i + 2] - prices[i + 1]
        c2 = prices[i + 3] - prices[i + 2]
        c3 = prices[i + 4] - prices[i + 3]
        pattern = (c0, c1, c2, c3)

        if pattern not in pattern_dict:
            # earliest price we can sell at if we see this pattern
            pattern_dict[pattern] = prices[i + 4]

    return pattern_dict


def part1(buyers):
    """
    Same as before: for each buyer, evolve the secret 2000 times
    and sum the final secrets.
    """
    total = 0
    for s in buyers:
        for _ in range(2000):
            s = evolve(s)
        total += s
    return total


def part2(buyers):
    """
    For Part 2:
      1) For each buyer, generate 2001 prices (the ones digit of each secret).
      2) Build a dictionary mapping 4-change-pattern -> earliest sale price.
      3) Combine all buyers' dictionaries to find which single 4-change-pattern
         yields the maximum total bananas (sum of earliest sale prices from each buyer).
    """
    from collections import defaultdict

    # Build an aggregated mapping from pattern -> sum of earliest sale prices over ALL buyers
    aggregator = defaultdict(int)

    for initial_secret in buyers:
        # 1) Generate the buyer's 2001 prices
        prices = generate_prices(initial_secret, length=2000)

        # 2) Build that buyer's pattern dictionary
        buyer_dict = build_pattern_dict(prices)

        # 3) Merge into the aggregator
        for pattern, sale_price in buyer_dict.items():
            aggregator[pattern] += sale_price

    # The puzzle asks for the maximum sum we can get if we pick the best 4-change pattern
    max_bananas = max(aggregator.values()) if aggregator else 0
    return max_bananas


def main():
    data = read_data()

    # Part 1 result
    result1 = part1(data)
    print(result1)

    # Part 2 result
    result2 = part2(data)
    print(result2)


if __name__ == "__main__":
    main()
