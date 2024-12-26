import itertools


def read_data(filename):
    """Reads the input file and returns a set of connections."""
    connections = set()
    with open(filename, "r") as f:
        for line in f:
            a, b = line.strip().split("-")
            connections.add(
                tuple(sorted((a, b)))
            )  # Store as sorted tuples to avoid duplicates
    return connections


def part1(connections):
    """Finds sets of three interconnected computers and counts those with 't'."""
    computers = set()
    for a, b in connections:
        computers.add(a)
        computers.add(b)

    count_with_t = 0
    for combo in itertools.combinations(computers, 3):
        a, b, c = sorted(combo)  # Sort for consistent checking
        if (a, b) in connections and (a, c) in connections and (b, c) in connections:
            if any(comp.startswith("t") for comp in (a, b, c)):
                count_with_t += 1
    return count_with_t


def part2(connections):
    """Finds the largest set of interconnected computers and returns the password."""
    computers = set()
    for a, b in connections:
        computers.add(a)
        computers.add(b)

    max_set = set()
    for i in range(2, len(computers) + 1):  # Iterate through possible set sizes
        for combo in itertools.combinations(computers, i):
            is_connected = True
            for pair in itertools.combinations(combo, 2):
                if tuple(sorted(pair)) not in connections:
                    is_connected = False
                    break
            if is_connected:
                if len(combo) > len(max_set):
                    max_set = set(combo)

    return ",".join(sorted(max_set))


def main():
    connections = read_data("23.txt")
    result1 = part1(connections)
    print(result1)
    result2 = part2(connections)
    print(result2)


if __name__ == "__main__":
    main()
