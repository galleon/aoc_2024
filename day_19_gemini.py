import re


def read_data(filename):
    with open(filename, "r") as f:
        data = f.read().strip().split("\n\n")
    patterns = data[0].split(", ")
    designs = data[1].splitlines()
    return patterns, designs


def part1(data):
    patterns, designs = data
    count = 0
    for design in designs:
        dp = [False] * (len(design) + 1)
        dp[0] = True
        for i in range(len(design)):
            if dp[i]:
                for pattern in patterns:
                    if design[i:].startswith(pattern):
                        dp[i + len(pattern)] = True
        if dp[len(design)]:
            count += 1
    return count


def main():
    data = read_data("19.txt")
    result = part1(data)
    print(result)


if __name__ == "__main__":
    main()
