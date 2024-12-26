def read_data():
    with open("19.txt", "r") as f:
        # Read all non-empty lines (strip whitespace and skip blanks)
        lines = [line.strip() for line in f if line.strip()]

    # First line holds the comma-separated towel patterns
    patterns = [p.strip() for p in lines[0].split(",")]
    # Remaining lines are the desired designs
    designs = lines[1:]
    return patterns, designs


def part1(data):
    patterns, designs = data

    from collections import deque

    def can_form(design):
        queue = deque([0])
        visited = set([0])
        while queue:
            start = queue.popleft()
            if start == len(design):
                return True
            for p in patterns:
                if design.startswith(p, start):
                    new_pos = start + len(p)
                    if new_pos not in visited:
                        visited.add(new_pos)
                        queue.append(new_pos)
        return False

    return sum(can_form(d) for d in designs)


def part2(data):
    patterns, designs = data

    def count_ways(design):
        ways = [0] * (len(design) + 1)
        ways[0] = 1  # There's exactly 1 way to form an empty prefix

        for i in range(len(design)):
            if ways[i] > 0:
                # Check which patterns match at index i
                for p in patterns:
                    if design.startswith(p, i):
                        ways[i + len(p)] += ways[i]

        return ways[len(design)]

    # Sum the number of ways for each design
    return sum(count_ways(d) for d in designs)


def main():
    data = read_data()
    print(part1(data))  # Print part1's result only
    print(part2(data))  # Print part2's result only


if __name__ == "__main__":
    main()
