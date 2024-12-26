from collections import defaultdict


def read_data(filename="19.txt"):
    with open(filename) as f:
        patterns, designs = f.read().strip().split("\n\n")
    patterns = [p.strip() for p in patterns.split(",")]
    designs = designs.strip().split("\n")
    return patterns, designs


def can_make_design(design, patterns, dp_cache=None):
    if dp_cache is None:
        dp_cache = {}

    if not design:
        return True
    if design in dp_cache:
        return dp_cache[design]

    for pattern in patterns:
        if design.startswith(pattern):
            if can_make_design(design[len(pattern) :], patterns, dp_cache):
                dp_cache[design] = True
                return True

    dp_cache[design] = False
    return False


def part1(data):
    patterns, designs = data
    possible_count = sum(1 for design in designs if can_make_design(design, patterns))
    return possible_count


def main():
    data = read_data()
    result = part1(data)
    print(f"Part 1: {result}")


if __name__ == "__main__":
    main()
